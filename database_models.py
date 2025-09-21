"""
MARGEN AI - Database Models
SQLite database schema for the MARGEN AI Career Advisor application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

# -----------------------------------------------------------------------------
# User Management Models
# -----------------------------------------------------------------------------

class User(db.Model):
    """User accounts with authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    user_skills = db.relationship('UserSkill', backref='user', lazy=True, cascade='all, delete-orphan')
    user_interests = db.relationship('UserInterest', backref='user', lazy=True, cascade='all, delete-orphan')
    career_recommendations = db.relationship('CareerRecommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    user_progress = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    learning_sessions = db.relationship('LearningSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_completed': self.profile_completed
        }

class OTP(db.Model):
    """OTP verification codes"""
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False, index=True)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    def is_expired(self):
        """Check if OTP is expired"""
        return datetime.utcnow() > self.expires_at

# -----------------------------------------------------------------------------
# Skills and Interests Models
# -----------------------------------------------------------------------------

class Skill(db.Model):
    """Master skills database"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # technical, soft, domain
    subcategory = db.Column(db.String(50), nullable=True)  # programming, communication, etc.
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_skills = db.relationship('UserSkill', backref='skill', lazy=True)
    career_skills = db.relationship('CareerSkill', backref='skill', lazy=True)

class UserSkill(db.Model):
    """User skills with proficiency levels"""
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    proficiency_level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced, expert
    confidence_score = db.Column(db.Integer, nullable=False)  # 1-10 scale
    years_experience = db.Column(db.Float, default=0.0)
    last_practiced = db.Column(db.DateTime, nullable=True)
    projects_count = db.Column(db.Integer, default=0)
    certifications = db.Column(db.Text, nullable=True)  # JSON string
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_id', name='unique_user_skill'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill.name,
            'skill_category': self.skill.category,
            'proficiency_level': self.proficiency_level,
            'confidence_score': self.confidence_score,
            'years_experience': self.years_experience,
            'last_practiced': self.last_practiced.isoformat() if self.last_practiced else None,
            'projects_count': self.projects_count,
            'certifications': json.loads(self.certifications) if self.certifications else [],
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Interest(db.Model):
    """Master interests database"""
    __tablename__ = 'interests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_interests = db.relationship('UserInterest', backref='interest', lazy=True)

class UserInterest(db.Model):
    """User interests with intensity levels"""
    __tablename__ = 'user_interests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), nullable=False)
    intensity_level = db.Column(db.String(20), nullable=False)  # low, medium, high, very_high
    confidence_score = db.Column(db.Integer, nullable=False)  # 1-10 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'interest_id', name='unique_user_interest'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'interest_name': self.interest.name,
            'interest_category': self.interest.category,
            'intensity_level': self.intensity_level,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# -----------------------------------------------------------------------------
# Career and Recommendations Models
# -----------------------------------------------------------------------------

class Career(db.Model):
    """Master careers database"""
    __tablename__ = 'careers'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    estimated_duration = db.Column(db.String(50), nullable=True)
    salary_range_min = db.Column(db.Integer, nullable=True)
    salary_range_max = db.Column(db.Integer, nullable=True)
    job_market_demand = db.Column(db.String(20), nullable=True)  # low, medium, high
    growth_rate = db.Column(db.Float, nullable=True)  # percentage
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    career_skills = db.relationship('CareerSkill', backref='career', lazy=True, cascade='all, delete-orphan')
    career_recommendations = db.relationship('CareerRecommendation', backref='career', lazy=True)
    roadmaps = db.relationship('Roadmap', backref='career', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'estimated_duration': self.estimated_duration,
            'salary_range_min': self.salary_range_min,
            'salary_range_max': self.salary_range_max,
            'job_market_demand': self.job_market_demand,
            'growth_rate': self.growth_rate,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CareerSkill(db.Model):
    """Skills required for careers"""
    __tablename__ = 'career_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    importance_level = db.Column(db.String(20), nullable=False)  # required, important, nice_to_have
    proficiency_required = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced, expert
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('career_id', 'skill_id', name='unique_career_skill'),)

class CareerRecommendation(db.Model):
    """AI-generated career recommendations for users"""
    __tablename__ = 'career_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    match_percentage = db.Column(db.Float, nullable=False)  # 0-100
    confidence_score = db.Column(db.Float, nullable=False)  # 0-1
    ai_reasons = db.Column(db.Text, nullable=True)  # JSON string with AI reasoning
    skill_gaps = db.Column(db.Text, nullable=True)  # JSON string with skill gaps
    learning_priority = db.Column(db.String(20), nullable=False)  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'career': self.career.to_dict(),
            'match_percentage': self.match_percentage,
            'confidence_score': self.confidence_score,
            'ai_reasons': json.loads(self.ai_reasons) if self.ai_reasons else [],
            'skill_gaps': json.loads(self.skill_gaps) if self.skill_gaps else [],
            'learning_priority': self.learning_priority,
            'created_at': self.created_at.isoformat()
        }

# -----------------------------------------------------------------------------
# Learning and Progress Models
# -----------------------------------------------------------------------------

class Roadmap(db.Model):
    """Learning roadmaps for careers"""
    __tablename__ = 'roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    phase_order = db.Column(db.Integer, nullable=False)
    estimated_duration = db.Column(db.String(50), nullable=True)
    difficulty_level = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    roadmap_skills = db.relationship('RoadmapSkill', backref='roadmap', lazy=True, cascade='all, delete-orphan')
    user_progress = db.relationship('UserProgress', backref='roadmap', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'career_id': self.career_id,
            'title': self.title,
            'description': self.description,
            'phase_order': self.phase_order,
            'estimated_duration': self.estimated_duration,
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class RoadmapSkill(db.Model):
    """Skills within roadmaps"""
    __tablename__ = 'roadmap_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    skill_order = db.Column(db.Integer, nullable=False)
    skill_type = db.Column(db.String(20), nullable=False)  # recommended, alternative
    description = db.Column(db.Text, nullable=True)
    resource_name = db.Column(db.String(200), nullable=True)
    resource_link = db.Column(db.String(500), nullable=True)
    is_required = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skill = db.relationship('Skill', backref='roadmap_skills')

class UserProgress(db.Model):
    """User progress tracking"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=True)
    progress_type = db.Column(db.String(20), nullable=False)  # skill, roadmap, career
    status = db.Column(db.String(20), nullable=False)  # not_started, in_progress, completed
    completion_percentage = db.Column(db.Float, default=0.0)  # 0-100
    time_spent_minutes = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skill = db.relationship('Skill', backref='user_progress')
    
    def to_dict(self):
        return {
            'id': self.id,
            'progress_type': self.progress_type,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'time_spent_minutes': self.time_spent_minutes,
            'notes': self.notes,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class LearningSession(db.Model):
    """Learning session tracking"""
    __tablename__ = 'learning_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_type = db.Column(db.String(20), nullable=False)  # skill_practice, roadmap_study, career_exploration
    duration_minutes = db.Column(db.Integer, nullable=False)
    skills_practiced = db.Column(db.Text, nullable=True)  # JSON string
    achievements = db.Column(db.Text, nullable=True)  # JSON string
    notes = db.Column(db.Text, nullable=True)
    session_data = db.Column(db.Text, nullable=True)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_type': self.session_type,
            'duration_minutes': self.duration_minutes,
            'skills_practiced': json.loads(self.skills_practiced) if self.skills_practiced else [],
            'achievements': json.loads(self.achievements) if self.achievements else [],
            'notes': self.notes,
            'session_data': json.loads(self.session_data) if self.session_data else {},
            'created_at': self.created_at.isoformat()
        }

# -----------------------------------------------------------------------------
# AI and Analytics Models
# -----------------------------------------------------------------------------

class AIInteraction(db.Model):
    """Track AI interactions and responses"""
    __tablename__ = 'ai_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    interaction_type = db.Column(db.String(50), nullable=False)  # career_generation, skill_analysis, roadmap_creation
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)  # gemini-pro, etc.
    tokens_used = db.Column(db.Integer, nullable=True)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    user_satisfaction = db.Column(db.Integer, nullable=True)  # 1-5 rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'interaction_type': self.interaction_type,
            'prompt': self.prompt,
            'response': self.response,
            'model_used': self.model_used,
            'tokens_used': self.tokens_used,
            'processing_time_ms': self.processing_time_ms,
            'user_satisfaction': self.user_satisfaction,
            'created_at': self.created_at.isoformat()
        }

class UserAnalytics(db.Model):
    """User behavior and analytics"""
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # page_view, feature_use, career_click, etc.
    event_data = db.Column(db.Text, nullable=True)  # JSON string
    session_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'event_data': json.loads(self.event_data) if self.event_data else {},
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat()
        }

# -----------------------------------------------------------------------------
# Database Initialization Functions
# -----------------------------------------------------------------------------

def init_database(app):
    """Initialize database with app"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Insert initial data
        insert_initial_data()
        print("✅ Initial data inserted successfully")

def insert_initial_data():
    """Insert initial data into database"""
    
    # Insert initial skills
    initial_skills = [
        # Technical Skills
        {'name': 'Python', 'category': 'technical', 'subcategory': 'programming', 'description': 'Python programming language'},
        {'name': 'JavaScript', 'category': 'technical', 'subcategory': 'programming', 'description': 'JavaScript programming language'},
        {'name': 'React', 'category': 'technical', 'subcategory': 'frameworks', 'description': 'React.js framework'},
        {'name': 'Node.js', 'category': 'technical', 'subcategory': 'frameworks', 'description': 'Node.js runtime'},
        {'name': 'SQL', 'category': 'technical', 'subcategory': 'databases', 'description': 'SQL database language'},
        {'name': 'Git', 'category': 'technical', 'subcategory': 'tools', 'description': 'Version control system'},
        {'name': 'Docker', 'category': 'technical', 'subcategory': 'tools', 'description': 'Containerization platform'},
        {'name': 'AWS', 'category': 'technical', 'subcategory': 'cloud', 'description': 'Amazon Web Services'},
        
        # Soft Skills
        {'name': 'Communication', 'category': 'soft', 'subcategory': 'interpersonal', 'description': 'Verbal and written communication'},
        {'name': 'Leadership', 'category': 'soft', 'subcategory': 'management', 'description': 'Team leadership and management'},
        {'name': 'Problem Solving', 'category': 'soft', 'subcategory': 'analytical', 'description': 'Analytical problem solving'},
        {'name': 'Teamwork', 'category': 'soft', 'subcategory': 'interpersonal', 'description': 'Collaborative working'},
        {'name': 'Time Management', 'category': 'soft', 'subcategory': 'productivity', 'description': 'Effective time management'},
        
        # Domain Skills
        {'name': 'Data Analysis', 'category': 'domain', 'subcategory': 'analytics', 'description': 'Data analysis and interpretation'},
        {'name': 'Machine Learning', 'category': 'domain', 'subcategory': 'ai', 'description': 'Machine learning algorithms'},
        {'name': 'UI/UX Design', 'category': 'domain', 'subcategory': 'design', 'description': 'User interface and experience design'},
        {'name': 'Project Management', 'category': 'domain', 'subcategory': 'management', 'description': 'Project planning and execution'},
    ]
    
    for skill_data in initial_skills:
        if not Skill.query.filter_by(name=skill_data['name']).first():
            skill = Skill(**skill_data)
            db.session.add(skill)
    
    # Insert initial interests
    initial_interests = [
        {'name': 'Artificial Intelligence', 'category': 'technology', 'description': 'AI and machine learning'},
        {'name': 'Web Development', 'category': 'technology', 'description': 'Building web applications'},
        {'name': 'Data Science', 'category': 'technology', 'description': 'Data analysis and insights'},
        {'name': 'Mobile Development', 'category': 'technology', 'description': 'Mobile app development'},
        {'name': 'Cybersecurity', 'category': 'technology', 'description': 'Information security'},
        {'name': 'Design', 'category': 'creative', 'description': 'Visual and user experience design'},
        {'name': 'Business', 'category': 'professional', 'description': 'Business strategy and management'},
        {'name': 'Healthcare', 'category': 'industry', 'description': 'Healthcare and medical technology'},
        {'name': 'Finance', 'category': 'industry', 'description': 'Financial services and fintech'},
        {'name': 'Education', 'category': 'industry', 'description': 'Educational technology'},
    ]
    
    for interest_data in initial_interests:
        if not Interest.query.filter_by(name=interest_data['name']).first():
            interest = Interest(**interest_data)
            db.session.add(interest)
    
    # Insert initial careers
    initial_careers = [
        {
            'title': 'Frontend Developer',
            'description': 'Create user interfaces and user experiences for web applications',
            'category': 'Development',
            'difficulty_level': 'intermediate',
            'estimated_duration': '6-8 months',
            'salary_range_min': 60000,
            'salary_range_max': 120000,
            'job_market_demand': 'high',
            'growth_rate': 15.0,
            'is_featured': True
        },
        {
            'title': 'Data Scientist',
            'description': 'Extract insights from data using statistics, machine learning, and programming',
            'category': 'Data Science',
            'difficulty_level': 'advanced',
            'estimated_duration': '9-12 months',
            'salary_range_min': 80000,
            'salary_range_max': 150000,
            'job_market_demand': 'high',
            'growth_rate': 22.0,
            'is_featured': True
        },
        {
            'title': 'DevOps Engineer',
            'description': 'Bridge development and operations to automate software delivery',
            'category': 'DevOps',
            'difficulty_level': 'intermediate',
            'estimated_duration': '7-9 months',
            'salary_range_min': 70000,
            'salary_range_max': 130000,
            'job_market_demand': 'high',
            'growth_rate': 18.0,
            'is_featured': False
        },
        {
            'title': 'Product Manager',
            'description': 'Lead product development from concept to launch',
            'category': 'Management',
            'difficulty_level': 'intermediate',
            'estimated_duration': '8-10 months',
            'salary_range_min': 90000,
            'salary_range_max': 160000,
            'job_market_demand': 'medium',
            'growth_rate': 12.0,
            'is_featured': True
        }
    ]
    
    for career_data in initial_careers:
        if not Career.query.filter_by(title=career_data['title']).first():
            career = Career(**career_data)
            db.session.add(career)
    
    # Commit all changes
    db.session.commit()
    print("✅ Initial data inserted successfully")

# -----------------------------------------------------------------------------
# Database Utility Functions
# -----------------------------------------------------------------------------

def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()

def get_user_by_phone(phone):
    """Get user by phone"""
    return User.query.filter_by(phone=phone).first()

def create_user(email, password, phone=None, first_name=None, last_name=None):
    """Create a new user"""
    user = User(
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def log_ai_interaction(user_id, interaction_type, prompt, response, model_used, tokens_used=None, processing_time_ms=None):
    """Log AI interaction for analytics"""
    interaction = AIInteraction(
        user_id=user_id,
        interaction_type=interaction_type,
        prompt=prompt,
        response=response,
        model_used=model_used,
        tokens_used=tokens_used,
        processing_time_ms=processing_time_ms
    )
    db.session.add(interaction)
    db.session.commit()
    return interaction

def log_user_analytics(user_id, event_type, event_data=None, session_id=None, ip_address=None, user_agent=None):
    """Log user analytics event"""
    analytics = UserAnalytics(
        user_id=user_id,
        event_type=event_type,
        event_data=json.dumps(event_data) if event_data else None,
        session_id=session_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.session.add(analytics)
    db.session.commit()
    return analytics
