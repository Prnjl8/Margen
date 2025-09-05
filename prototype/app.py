import os
import random
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.rest import Client
import google.generativeai as genai
from dotenv import load_dotenv
import re
from werkzeug.security import generate_password_hash, check_password_hash

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
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None

# Gemini AI Configuration
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

# --- 2. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)

with app.app_context():
    db.create_all()

# --- 3. HELPER FUNCTION (IMPROVED) ---
def clean_json_response(text):
    """More robustly cleans the AI's response to extract valid JSON."""
    match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    
    start_bracket_pos = text.find('[')
    start_brace_pos = text.find('{')
    
    if start_bracket_pos == -1 and start_brace_pos == -1: return text
    
    start_pos = -1
    if start_bracket_pos != -1 and start_brace_pos != -1: start_pos = min(start_bracket_pos, start_brace_pos)
    elif start_bracket_pos != -1: start_pos = start_bracket_pos
    else: start_pos = start_brace_pos

    end_char = ']' if text[start_pos] == '[' else '}'
    end_pos = text.rfind(end_char)

    if end_pos > start_pos: return text[start_pos:end_pos + 1]
    
    return text

# --- 4. API ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# --- AUTHENTICATION ROUTES ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "identifier": user.email}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/send-otp', methods=['POST'])
def send_otp():
    if not twilio_client: return jsonify({"error": "Twilio client not configured."}), 500
    data = request.get_json()
    phone = data['phone']
    otp_code = str(random.randint(100000, 999999))
    existing_otp = OTP.query.filter_by(phone=phone).first()
    if existing_otp: existing_otp.otp_code = otp_code
    else: db.session.add(OTP(phone=phone, otp_code=otp_code))
    db.session.commit()
    try:
        twilio_client.messages.create(body=f"Your MARGEN AI verification code is: {otp_code}", from_=TWILIO_PHONE_NUMBER, to=phone)
        return jsonify({"message": f"OTP sent to {phone}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP. Check phone format and Twilio setup."}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp_entry = OTP.query.filter_by(phone=data['phone'], otp_code=data['code']).first()
    if otp_entry:
        return jsonify({"message": "Login successful", "identifier": data['phone']}), 200
    return jsonify({"error": "Invalid OTP code"}), 401

# --- CORE AI ROUTES ---
@app.route('/generate-careers', methods=['POST'])
def generate_careers():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    prompt = f"""
    Based on the user profile:
    - Name: "{data.get('name', 'N/A')}"
    - Interests: "{data.get('interests', 'Not specified')}"
    - Skills: "{data.get('skills', 'Not specified')}"
    - Preferred Pace: "{data.get('pace', 'Balanced')}"
    - Life Goals: "{', '.join(data.get('lifeGoals', []))}"
    Generate a diverse list of 7 creative and professional career options.
    Respond ONLY with a valid JSON array of objects. Each object must have a "title" and a "description".
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": f"AI returned invalid JSON for careers: {e}"}), 500

@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    prompt = f"""
    Create a detailed, step-by-step learning roadmap for a "{data['careerTitle']}".
    The roadmap should have 3-5 major milestones.
    For each milestone, provide a "title" and a list of "skills". Each skill in the list should be an object with a "name" and a "resource" object. The "resource" object must have a "name" (e.g., "Udemy Course") and a direct, clickable "link".
    Respond ONLY with a valid JSON array of these milestone objects.
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": f"AI returned invalid JSON for roadmap: {e}"}), 500

# --- NEW FEATURE ROUTES ---

@app.route('/find-interests', methods=['POST'])
def find_interests():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json().get('answers', {})
    prompt = f"""
    A user has answered an interest assessment quiz. Based on their answers below, analyze their personality and generate a comma-separated list of 3 to 5 likely interests.
    Answers:
    1. On a free weekend, they'd be: {data.get('q1', 'not answered')}
    2. Fascinating topic: {data.get('q2', 'not answered')}
    3. Enjoys tasks involving: {data.get('q3', 'not answered')}
    4. New project idea: {data.get('q4', 'not answered')}
    5. Comfortable working with: {data.get('q5', 'not answered')}
    Respond ONLY with the comma-separated list of interests.
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"interests": response.text.strip()})
    except Exception as e:
        return jsonify({"error": f"Could not analyze interests: {e}"}), 500

@app.route('/get-case-studies', methods=['POST'])
def get_case_studies():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    career_title = data.get('careerTitle')
    # CORRECTED PROMPT FOR CASE STUDIES
    prompt = f"""
    For the career of '{career_title}', generate profiles for 3 realistic professional archetypes.
    For each profile, provide:
    - "name": A realistic fictional name.
    - "title": Their specific job title.
    - "photo": A placeholder URL from i.pravatar.cc.
    - "journey": A short narrative (60-80 words) about their career journey.
    - "keySkills": An array of 3-4 key skills they use daily.
    - "proTip": A single, actionable "pro tip" (15-25 words).
    - "resource": An object with a "type" ('video' or 'article') and a real, relevant "link" to a YouTube video or an insightful article about this career path.

    Respond ONLY with a valid JSON array of these 3 case study objects.
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": f"AI returned invalid JSON for case studies: {e}"}), 500

@app.route('/analyze-skills', methods=['POST'])
def analyze_skills():
    data = request.get_json()
    user_skills_raw = data.get('userSkills', '')
    roadmap = data.get('roadmap', [])
    if not user_skills_raw or not roadmap:
        return jsonify({"error": "Missing user skills or roadmap data."}), 400
    user_skills = {s.strip().lower() for s in user_skills_raw.split(',') if s.strip()}
    required_skills = {skill['name'].lower() for milestone in roadmap for skill in milestone.get('skills', [])}
    skills_have = {req_skill for req_skill in required_skills if any(user_skill in req_skill for user_skill in user_skills)}
    skills_to_learn = required_skills - skills_have
    percentage = round((len(skills_have) / len(required_skills)) * 100) if required_skills else 0
    return jsonify({
        "percentage": percentage,
        "skillsHave": sorted(list(skills_have)),
        "skillsToLearn": sorted(list(skills_to_learn))
    })
    
@app.route('/generate-comparison', methods=['POST'])
def generate_comparison():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    career_titles = data.get('careerTitles', [])
    
    prompt = f"""
    For the following list of careers: {', '.join(career_titles)}, generate a brief, point-by-point comparison roadmap for each.
    For each career, provide a "title" and a "summary_roadmap" which is an array of 2-3 milestone objects.
    Each milestone object should have a "title" (e.g., "Foundations") and a short "description" (e.g., "Learn core concepts and tools.").
    Respond ONLY with a valid JSON array of objects, where each object represents a career.
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": f"AI returned invalid JSON for comparison: {e}"}), 500

# --- 5. RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)

