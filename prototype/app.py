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
# A more robust way to define the template folder
app = Flask(__name__, template_folder='templates') 
CORS(app) 

# Database Configuration
# Using an absolute path is more reliable for web servers.
# It will create the database file in the same directory as this script.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None

# Gemini AI Configuration
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

# --- 2. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    # New field to store user profile data as JSON
    profile_data = db.Column(db.Text, nullable=True)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)

with app.app_context():
    db.create_all()

# --- 3. HELPER FUNCTION ---
def clean_json_response(text):
    """More robustly cleans the AI's response to extract valid JSON."""
    match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    
    # Find the first '[' or '{' and the last ']' or '}'
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

# ADDED: Root route to serve the frontend HTML file
@app.route('/')
def index():
    # This tells Flask to find and return 'index2.html' from the 'templates' folder
    return render_template('index2.html')

# --- AUTHENTICATION & USER DATA ROUTES ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400
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
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "identifier": user.email}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/send-otp', methods=['POST'])
def send_otp():
    if not twilio_client: return jsonify({"error": "Twilio client not configured on the server."}), 500
    data = request.get_json()
    phone = data.get('phone')
    if not phone: return jsonify({"error": "Phone number is required"}), 400

    otp_code = str(random.randint(100000, 999999))
    existing_otp = OTP.query.filter_by(phone=phone).first()
    if existing_otp: existing_otp.otp_code = otp_code
    else: db.session.add(OTP(phone=phone, otp_code=otp_code))
    db.session.commit()
    try:
        twilio_client.messages.create(body=f"Your MARGEN AI verification code is: {otp_code}", from_=TWILIO_PHONE_NUMBER, to=phone)
        return jsonify({"message": f"OTP sent to {phone}"}), 200
    except Exception as e:
        print(f"Twilio Error: {e}")
        return jsonify({"error": f"Failed to send OTP. Please check phone number format and server setup."}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    if not data or 'phone' not in data or 'code' not in data:
        return jsonify({"error": "Phone number and OTP code are required"}), 400
    otp_entry = OTP.query.filter_by(phone=data['phone'], otp_code=data['code']).first()
    if otp_entry:
        # OTP is correct, log the user in (or create an account if it doesn't exist)
        return jsonify({"message": "Login successful", "identifier": data['phone']}), 200
    return jsonify({"error": "Invalid OTP code"}), 401

@app.route('/save-profile', methods=['POST'])
def save_profile():
    data = request.get_json()
    email = data.get('email')
    profile_data = data.get('profile') # This will be the dict with interests, skills etc.
    if not email or not profile_data:
        return jsonify({"error": "Email and profile data are required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.profile_data = json.dumps(profile_data)
        db.session.commit()
        return jsonify({"message": "Profile saved successfully"}), 200
    return jsonify({"error": "User not found"}), 404


# --- CORE AI ROUTES ---
@app.route('/find-interests', methods=['POST'])
def find_interests():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json().get('answers', {})
    prompt = f"""
    Analyze a user's personality based on their answers to an interest assessment quiz.
    Based on these answers, generate a comma-separated list of 3 to 5 highly relevant interests for them.
    The interests should be concise and professional (e.g., "Data Analysis, Creative Design, Project Management").

    User's Answers:
    1. On a free weekend, they'd be: {data.get('q1', 'not answered')}
    2. Fascinating topic: {data.get('q2', 'not answered')}
    3. Enjoys tasks involving: {data.get('q3', 'not answered')}
    4. New project idea: {data.get('q4', 'not answered')}
    5. Comfortable working with: {data.get('q5', 'not answered')}

    Respond ONLY with the comma-separated list of interests and nothing else.
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"interests": response.text.strip()})
    except Exception as e:
        print(f"Gemini Error in /find-interests: {e}")
        return jsonify({"error": f"Could not analyze interests due to a server error."}), 500

@app.route('/generate-careers', methods=['POST'])
def generate_careers():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    prompt = f"""
    Based on the following user profile, generate a diverse list of 7 creative and professional career path recommendations.
    - Interests: "{data.get('interests', 'Not specified')}"
    - Skills: "{data.get('skills', 'Not specified')}"
    - Preferred Pace: "{data.get('pace', 'Balanced')}"
    - Life Goals: "{', '.join(data.get('lifeGoals', []))}"

    For each recommendation, provide a "title" and a short, compelling "description" (around 15-20 words).
    Respond ONLY with a valid JSON array of objects. Each object must have a "title" and a "description". Do not include any other text or markdown.
    Example format:
    [
      {{"title": "AI Ethics Consultant", "description": "Guide companies in the responsible development and deployment of artificial intelligence systems."}},
      {{"title": "UX/UI Designer", "description": "Craft intuitive and visually appealing digital experiences for users."}}
    ]
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        print(f"Gemini Error in /generate-careers: {e}")
        return jsonify({"error": f"AI returned an invalid response for careers. Please try again."}), 500

@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    career_title = data.get('careerTitle', 'the selected career')
    
    prompt = f"""
    You are an expert career advisor. Create a detailed, step-by-step learning roadmap for a user aspiring to become a "{career_title}".
    The roadmap must be structured as a JSON array of 3 to 5 major milestone objects.

    Each milestone object in the array must contain:
    1. A "title" (string): A clear and concise name for the milestone (e.g., "Foundational Knowledge", "Framework Mastery", "Advanced Skills & Portfolio").
    2. A "skills" (array of objects): A list of key skills to learn in this milestone.

    Each skill object within the "skills" array must contain:
    1. A "name" (string): The name of the skill or technology (e.g., "JavaScript (ES6+)", "React State Management").
    2. A "resource" (object): A single, high-quality, real learning resource.

    Each resource object must contain:
    1. A "name" (string): The name of the resource provider or type (e.g., "Udemy Course", "Official Docs", "freeCodeCamp", "YouTube Tutorial").
    2. A "link" (string): A direct, valid, and clickable HTTPS URL to the resource.

    Respond ONLY with the valid JSON array of these milestone objects. Do not include any explanatory text, markdown formatting, or any other characters outside of the JSON structure.
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        print(f"Gemini Error in /generate-roadmap: {e}")
        return jsonify({"error": f"AI returned an invalid response for the roadmap. Please try again."}), 500
        
@app.route('/analyze-skills', methods=['POST'])
def analyze_skills():
    """
    This endpoint performs the skill gap analysis on the backend.
    The frontend should send the user's skills and the generated roadmap.
    """
    data = request.get_json()
    user_skills_raw = data.get('userSkills', '')
    roadmap = data.get('roadmap', [])
    if not user_skills_raw or not roadmap:
        return jsonify({"error": "Missing user skills or roadmap data."}), 400

    # Sanitize user skills: lowercase, trim whitespace, remove empty strings
    user_skills = {s.strip().lower() for s in user_skills_raw.split(',') if s.strip()}
    
    # Extract required skills from the roadmap
    required_skills = {skill['name'].lower() for milestone in roadmap for skill in milestone.get('skills', [])}
    
    # Find matches. A user skill matches if it's a substring of a required skill.
    skills_have = {req_skill for req_skill in required_skills if any(user_skill in req_skill for user_skill in user_skills)}
    skills_to_learn = required_skills - skills_have
    
    percentage = round((len(skills_have) / len(required_skills)) * 100) if required_skills else 0
    
    # Capitalize for display
    def capitalize_skill(s):
        return ' '.join(word.capitalize() for word in s.split())

    return jsonify({
        "percentage": percentage,
        "skillsHave": sorted(list(map(capitalize_skill, skills_have))),
        "skillsToLearn": sorted(list(map(capitalize_skill, skills_to_learn)))
    })

@app.route('/generate-project-pitch', methods=['POST'])
def generate_project_pitch():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    interests = data.get('interests', 'general topics')
    skills = data.get('skills', [])
    milestone_title = data.get('milestoneTitle', 'the current milestone')

    if not skills:
        return jsonify({"error": "Skills are required for a project pitch."}), 400

    prompt = f"""
    Based on a user's interest in "{interests}" and the required skills for the milestone "{milestone_title}" which are [{', '.join(skills)}], generate a single, creative, and actionable project idea.
    The project idea should help the user practice the specified skills.
    Describe the project in a concise paragraph (about 50-70 words).
    
    Respond ONLY with a valid JSON object containing a single key "pitch" with the project description as its value.
    Example: {{"pitch": "Build an interactive portfolio website using React. This site could dynamically showcase your projects, filtering them based on the technologies used, and include a blog section where you write about your learning journey."}}
    """
    try:
        response = model.generate_content(prompt)
        json_data = json.loads(clean_json_response(response.text))
        return jsonify(json_data)
    except Exception as e:
        print(f"Gemini Error in /generate-project-pitch: {e}")
        return jsonify({"error": "AI failed to generate a project pitch."}), 500

# --- NEW MOCK INTERVIEW ROUTES ---
@app.route('/start-interview', methods=['POST'])
def start_interview():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    career_title = data.get('careerTitle', 'the selected field')
    prompt = f"""
    You are an expert, friendly hiring manager conducting a mock interview for a "{career_title}" position.
    Start the interview with a welcoming greeting and then ask your first, open-ended question to gauge the candidate's interest and background.
    Keep your response to a single, concise paragraph.
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"greeting": response.text.strip()})
    except Exception as e:
        print(f"Gemini Error in /start-interview: {e}")
        return jsonify({"error": "Failed to start the interview due to a server error."}), 500

@app.route('/continue-interview', methods=['POST'])
def continue_interview():
    if not model: return jsonify({"error": "AI model not configured"}), 500
    data = request.get_json()
    career_title = data.get('careerTitle', 'the selected field')
    conversation = data.get('conversation', [])
    
    # Format the conversation history for the AI
    history_text = ""
    for turn in conversation:
        role = "You (Interviewer)" if turn['role'] == 'model' else "Candidate"
        history_text += f"{role}: {turn['parts'][0]['text']}\n"
        
    prompt = f"""
    You are an expert, friendly hiring manager continuing a mock interview for a "{career_title}" position.
    Here is the conversation so far:
    {history_text}
    Based on the candidate's last response, ask a relevant follow-up question or provide brief feedback. 
    Keep the conversation flowing naturally. Your response should be a single, concise paragraph.
    Do not repeat questions. Ask behavioral, situational, or technical questions as appropriate for the role.
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"text": response.text.strip()})
    except Exception as e:
        print(f"Gemini Error in /continue-interview: {e}")
        return jsonify({"error": "Failed to continue the interview due to a server error."}), 500

# --- 5. RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)

