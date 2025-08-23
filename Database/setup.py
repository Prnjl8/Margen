# test_database.py
import sqlite3
import os
from db_utils import DatabaseManager

def test_database_connection():
    """Test basic database connection and table existence"""
    print("=== Testing Database Connection ===")
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'margen_ai.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return False
    
    print(f"✅ Database file found at: {db_path}")
    
    # Test connection
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'user_profiles', 'careers', 'milestones', 'skills', 'milestone_skills']
        
        print(f"📋 Found tables: {tables}")
        
        for table in expected_tables:
            if table in tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_sample_data():
    """Test that sample data was properly inserted"""
    print("\n=== Testing Sample Data ===")
    
    db = DatabaseManager()
    
    # Test careers
    careers = db.get_all_careers()
    print(f"📊 Found {len(careers)} careers:")
    for career in careers:
        print(f"   - {career['title']}: {career['description'][:50]}...")
    
    # Test roadmap for Frontend Developer
    print(f"\n🗺️  Testing roadmap for Frontend Developer:")
    roadmap = db.get_career_roadmap(1)  # Frontend Developer has career_id = 1
    for milestone in roadmap:
        print(f"   {milestone['order']}. {milestone['title']}")
        print(f"      Skills: {', '.join(milestone['skills'])}")
    
    # Test skill search
    print(f"\n🔍 Testing skill-based career search:")
    matching_careers = db.search_careers_by_skills(['Python', 'SQL'])
    print(f"Careers matching 'Python' and 'SQL':")
    for career in matching_careers:
        print(f"   - {career['title']} ({career['skill_matches']} skill matches)")

def test_user_operations():
    """Test user creation and profile operations"""
    print("\n=== Testing User Operations ===")
    
    db = DatabaseManager()
    
    # Test creating a user
    test_email = "test@example.com"
    test_password_hash = "hashed_password_123"
    
    try:
        user_id = db.create_user(test_email, test_password_hash, "123-456-7890", "Bachelor's")
        print(f"✅ Created user with ID: {user_id}")
        
        # Test retrieving user
        user = db.get_user_by_email(test_email)
        if user:
            print(f"✅ Retrieved user: {user['email']} (ID: {user['user_id']})")
        
        # Test creating user profile
        profile_id = db.create_user_profile(user_id, "Coding, Design", "Python, JavaScript", "Problem-solving, Creativity")
        print(f"✅ Created profile with ID: {profile_id}")
        
        # Test retrieving profile
        profile = db.get_user_profile(user_id)
        if profile:
            print(f"✅ Retrieved profile: Interests={profile['interests']}")
        
        # Clean up test data
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        print("🧹 Cleaned up test data")
        
    except Exception as e:
        print(f"❌ User operations failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing AI Career Advisor Database\n")
    
    # Test 1: Database connection and structure
    if not test_database_connection():
        print("❌ Database connection test failed. Exiting.")
        return
    
    # Test 2: Sample data
    test_sample_data()
    
    # Test 3: User operations
    test_user_operations()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
