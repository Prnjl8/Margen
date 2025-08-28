# app.py
import os
import random
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.rest import Client
import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. INITIALIZATION & CONFIGURATION ---
load_dotenv()
app = Flask(__name__, template_folder='templates') 
CORS(app) 

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Gemini AI Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)

with app.app_context():
    db.create_all()

# --- 3. API ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful", "identifier": user.email}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = data['phone']
    otp_code = str(random.randint(100000, 999999))
    existing_otp = OTP.query.filter_by(phone=phone).first()
    if existing_otp:
        existing_otp.otp_code = otp_code
    else:
        new_otp = OTP(phone=phone, otp_code=otp_code)
        db.session.add(new_otp)
    db.session.commit()
    try:
        message = twilio_client.messages.create(
            body=f"Your MARGEN AI verification code is: {otp_code}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        return jsonify({"message": f"OTP sent to {phone}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP. Check phone format."}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone = data['phone']
    code = data['code']
    otp_entry = OTP.query.filter_by(phone=phone, otp_code=code).first()
    if otp_entry:
        return jsonify({"message": "Login successful", "identifier": phone}), 200
    return jsonify({"error": "Invalid OTP code"}), 401

@app.route('/generate-careers', methods=['POST'])
def generate_careers():
    data = request.get_json()
    prompt = f"""
    Based on the user profile:
    - Name: "{data.get('name', 'N/A')}"
    - Interests: "{data['interests']}"
    - Skills: "{data['skills']}"
    - Preferred Pace: "{data['pace']}"
    - Life Goals: "{', '.join(data['lifeGoals'])}"

    Generate a diverse list of 7 creative and professional career options.
    Respond ONLY with a valid JSON array of objects. Each object must have a "title" and a "description".
    """
    try:
        response = model.generate_content(prompt)
        # FIX: Added more robust JSON cleaning
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:-3]
        
        return jsonify(json.loads(cleaned_text))
    except Exception as e:
        print(f"Error generating careers: {e}")
        print(f"Problematic AI response: {response.text}")
        return jsonify({"error": "Could not generate careers from AI."}), 500

@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap():
    data = request.get_json()
    prompt = f"""
    Create a concise, point-by-point learning roadmap for a "{data['careerTitle']}".
    The roadmap should have 3-4 major milestones.
    For each milestone, provide a "title" and a list of "skills".
    For each skill in the "skills" list, provide a "name" and a "resource" object with a "name" (e.g., "Udemy Course", "YouTube Tutorial") and a "link" (a direct, real URL).
    Respond ONLY with a valid JSON array of milestone objects.

    Example format:
    [
      {{
        "title": "Foundational Knowledge",
        "skills": [
          {{ "name": "HTML5 & CSS3", "resource": {{ "name": "freeCodeCamp", "link": "[https://www.freecodecamp.org/learn/2022/responsive-web-design/](https://www.freecodecamp.org/learn/2022/responsive-web-design/)" }} }},
          {{ "name": "JavaScript (ES6+)", "resource": {{ "name": "MDN Docs", "link": "[https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)" }} }}
        ]
      }}
    ]
    """
    try:
        response = model.generate_content(prompt)
        # FIX: Added more robust JSON cleaning
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:-3]
            
        return jsonify(json.loads(cleaned_text))
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        print(f"Problematic AI response: {response.text}")
        return jsonify({"error": "Could not generate roadmap from AI."}), 500

# --- 4. RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)
