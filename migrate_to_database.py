#!/usr/bin/env python3
"""
MARGEN AI - Migration Script
Migrate from mock data system to SQLite database
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask
from database_models import (
    db, User, Skill, Interest, Career, UserSkill, UserInterest,
    CareerRecommendation, init_database
)

def migrate_mock_data():
    """Migrate existing mock data to database"""
    print("🔄 Migrating mock data to database...")
    
    # Create Flask app for migration
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///margen_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'migration-key'
    
    with app.app_context():
        # Initialize database
        init_database(app)
        
        # Migrate mock users
        mock_users = {
            "test@example.com": "password123"
        }
        
        for email, password in mock_users.items():
            existing_user = User.query.filter_by(email=email).first()
            if not existing_user:
                user = User(email=email)
                user.set_password(password)
                user.is_verified = True
                user.profile_completed = True
                db.session.add(user)
                print(f"✅ Migrated user: {email}")
        
        # Migrate mock roadmap templates to careers
        mock_roadmaps = [
            {
                "id": "frontend-dev",
                "title": "Frontend Developer",
                "description": "Master the art of creating beautiful and interactive user interfaces for the web, following a path inspired by roadmap.sh.",
                "category": "Development",
                "difficulty": "intermediate",
                "estimated_duration": "6-8 Months",
                "is_featured": True
            },
            {
                "id": "data-scientist",
                "title": "Data Scientist", 
                "description": "Learn to extract meaningful insights from data using statistics, machine learning, and programming.",
                "category": "Data Science",
                "difficulty": "advanced",
                "estimated_duration": "9-12 Months",
                "is_featured": True
            },
            {
                "id": "devops-engineer",
                "title": "DevOps Engineer",
                "description": "Bridge the gap between development and operations to automate and streamline software delivery.",
                "category": "DevOps", 
                "difficulty": "intermediate",
                "estimated_duration": "7-9 Months",
                "is_featured": False
            }
        ]
        
        for roadmap_data in mock_roadmaps:
            existing_career = Career.query.filter_by(title=roadmap_data['title']).first()
            if not existing_career:
                career = Career(
                    title=roadmap_data['title'],
                    description=roadmap_data['description'],
                    category=roadmap_data['category'],
                    difficulty_level=roadmap_data['difficulty'],
                    estimated_duration=roadmap_data['estimated_duration'],
                    is_featured=roadmap_data['is_featured']
                )
                db.session.add(career)
                print(f"✅ Migrated career: {roadmap_data['title']}")
        
        # Commit all changes
        db.session.commit()
        print("✅ Migration completed successfully!")

def create_sample_data():
    """Create sample data for testing"""
    print("📊 Creating sample data...")
    
    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///margen_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sample-data-key'
    
    with app.app_context():
        # Create sample user
        sample_user = User(
            email="demo@margenai.com",
            first_name="Demo",
            last_name="User"
        )
        sample_user.set_password("demo123")
        sample_user.is_verified = True
        sample_user.profile_completed = True
        db.session.add(sample_user)
        db.session.flush()
        
        # Add sample skills
        sample_skills = [
            {"name": "Python", "proficiency": "intermediate", "confidence": 7},
            {"name": "JavaScript", "proficiency": "beginner", "confidence": 5},
            {"name": "React", "proficiency": "beginner", "confidence": 4},
            {"name": "Communication", "proficiency": "advanced", "confidence": 8}
        ]
        
        for skill_data in sample_skills:
            skill = Skill.query.filter_by(name=skill_data['name']).first()
            if skill:
                user_skill = UserSkill(
                    user_id=sample_user.id,
                    skill_id=skill.id,
                    proficiency_level=skill_data['proficiency'],
                    confidence_score=skill_data['confidence'],
                    years_experience=1.0,
                    projects_count=2
                )
                db.session.add(user_skill)
        
        # Add sample interests
        sample_interests = [
            {"name": "Web Development", "intensity": "high", "confidence": 8},
            {"name": "Artificial Intelligence", "intensity": "medium", "confidence": 6}
        ]
        
        for interest_data in sample_interests:
            interest = Interest.query.filter_by(name=interest_data['name']).first()
            if interest:
                user_interest = UserInterest(
                    user_id=sample_user.id,
                    interest_id=interest.id,
                    intensity_level=interest_data['intensity'],
                    confidence_score=interest_data['confidence']
                )
                db.session.add(user_interest)
        
        db.session.commit()
        print("✅ Sample data created successfully!")
        print(f"📧 Demo user: demo@margenai.com")
        print(f"🔑 Demo password: demo123")

def main():
    """Main migration function"""
    print("🚀 MARGEN AI Database Migration")
    print("=" * 50)
    
    try:
        # Check if database exists
        if os.path.exists('margen_ai.db'):
            print("⚠️  Database already exists!")
            response = input("Do you want to reset it? (y/N): ")
            if response.lower() == 'y':
                os.remove('margen_ai.db')
                print("🗑️  Old database removed")
            else:
                print("❌ Migration cancelled")
                return
        
        # Run migration
        migrate_mock_data()
        create_sample_data()
        
        print("\n🎉 Migration completed successfully!")
        print("📁 Database file: margen_ai.db")
        print("🚀 Ready to run: python backend/app_with_database.py")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
