#!/usr/bin/env python3
"""
Setup script for Career Advisor Database System
This script helps set up the database and check dependencies
"""

import os
import sys
import subprocess
import sqlite3

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_database():
    """Check if database exists and has data"""
    db_path = 'advisor.db'
    if not os.path.exists(db_path):
        print("❌ Database file not found. Creating database...")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("❌ Database exists but has no tables")
            conn.close()
            return False
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM careers")
        career_count = cursor.fetchone()[0]
        
        conn.close()
        
        if user_count == 0 or career_count == 0:
            print("❌ Database exists but has no data")
            return False
        
        print(f"✅ Database ready with {user_count} users and {career_count} careers")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def create_database():
    """Create the database and populate with sample data"""
    try:
        print("📝 Creating database...")
        subprocess.run([sys.executable, 'creat.db.py'], check=True)
        
        print("📝 Populating database with sample data...")
        subprocess.run([sys.executable, 'populate_db.py'], check=True)
        
        print("✅ Database created and populated successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating database: {e}")
        return False

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Backend dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
        return False

def install_backend_dependencies():
    """Install backend dependencies"""
    try:
        print("📦 Installing backend dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], check=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing backend dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Career Advisor Database System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check database
    if not check_database():
        if not create_database():
            sys.exit(1)
    
    # Check backend dependencies
    if not check_backend_dependencies():
        if not install_backend_dependencies():
            print("💡 You can install backend dependencies manually with:")
            print("   pip install -r backend/requirements.txt")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python app.py")
    print("\n2. In a new terminal, start the frontend:")
    print("   cd frontend")
    print("   npm install")
    print("   npm start")
    print("\n3. Open your browser to http://localhost:3000")

if __name__ == '__main__':
    main()
