#!/usr/bin/env python3
"""
MARGEN AI - Database Initialization Script
Initialize SQLite database with tables and initial data
"""

import os
import sys
from flask import Flask
from database_models import init_database, insert_initial_data, db

def main():
    """Initialize the database"""
    print("🚀 Initializing MARGEN AI Database...")
    print("=" * 50)
    
    # Create Flask app for database initialization
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///margen_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    try:
        # Initialize database
        init_database(app)
        
        print("✅ Database initialization completed successfully!")
        print(f"📁 Database file: {os.path.abspath('margen_ai.db')}")
        print("📊 Tables created:")
        print("   - users")
        print("   - otps") 
        print("   - skills")
        print("   - user_skills")
        print("   - interests")
        print("   - user_interests")
        print("   - careers")
        print("   - career_skills")
        print("   - career_recommendations")
        print("   - roadmaps")
        print("   - roadmap_skills")
        print("   - user_progress")
        print("   - learning_sessions")
        print("   - ai_interactions")
        print("   - user_analytics")
        
        print("\n🎯 Initial data inserted:")
        print("   - 18 technical skills")
        print("   - 10 interest categories")
        print("   - 4 sample careers")
        print("   - Database relationships configured")
        
        print("\n🚀 Ready to start the application!")
        print("Run: python backend/app_with_database.py")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
