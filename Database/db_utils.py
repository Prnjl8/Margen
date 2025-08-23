# db_utils.py
import sqlite3
import os
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to margen_ai.db in parent directory
            db_path = os.path.join(os.path.dirname(__file__), '..', 'margen_ai.db')
        self.db_path = db_path
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_all_careers(self) -> List[Dict]:
        """Get all careers with their descriptions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT career_id, title, description FROM careers ORDER BY title")
        careers = []
        for row in cursor.fetchall():
            careers.append({
                'career_id': row[0],
                'title': row[1],
                'description': row[2]
            })
        
        conn.close()
        return careers
    
    def get_career_milestones(self, career_id: int) -> List[Dict]:
        """Get all milestones for a specific career"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.milestone_id, m.title, m.milestone_order
            FROM milestones m
            WHERE m.career_id = ?
            ORDER BY m.milestone_order
        """, (career_id,))
        
        milestones = []
        for row in cursor.fetchall():
            milestones.append({
                'milestone_id': row[0],
                'title': row[1],
                'order': row[2]
            })
        
        conn.close()
        return milestones
    
    def get_milestone_skills(self, milestone_id: int) -> List[str]:
        """Get all skills for a specific milestone"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.name
            FROM skills s
            JOIN milestone_skills ms ON s.skill_id = ms.skill_id
            WHERE ms.milestone_id = ?
            ORDER BY s.name
        """, (milestone_id,))
        
        skills = [row[0] for row in cursor.fetchall()]
        conn.close()
        return skills
    
    def get_career_roadmap(self, career_id: int) -> List[Dict]:
        """Get complete roadmap for a career including milestones and skills"""
        milestones = self.get_career_milestones(career_id)
        
        for milestone in milestones:
            milestone['skills'] = self.get_milestone_skills(milestone['milestone_id'])
        
        return milestones
    
    def create_user(self, email: str, password_hash: str, phone_number: str = None, education_level: str = None) -> int:
        """Create a new user and return the user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, phone_number, education_level)
            VALUES (?, ?, ?, ?)
        """, (email, password_hash, phone_number, education_level))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def create_user_profile(self, user_id: int, interests: str, skills: str, aptitudes: str) -> int:
        """Create a user profile and return the profile_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_profiles (user_id, interests, skills, aptitudes)
            VALUES (?, ?, ?, ?)
        """, (user_id, interests, skills, aptitudes))
        
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return profile_id
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, email, password_hash, phone_number, education_level FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'user_id': row[0],
                'email': row[1],
                'password_hash': row[2],
                'phone_number': row[3],
                'education_level': row[4]
            }
        return None
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile by user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT profile_id, interests, skills, aptitudes FROM user_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'profile_id': row[0],
                'interests': row[1],
                'skills': row[2],
                'aptitudes': row[3]
            }
        return None
    
    def search_careers_by_skills(self, skills: List[str]) -> List[Dict]:
        """Search careers that match the given skills"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create placeholders for the IN clause
        placeholders = ','.join(['?' for _ in skills])
        
        cursor.execute(f"""
            SELECT DISTINCT c.career_id, c.title, c.description, COUNT(ms.skill_id) as skill_matches
            FROM careers c
            JOIN milestones m ON c.career_id = m.career_id
            JOIN milestone_skills ms ON m.milestone_id = ms.milestone_id
            JOIN skills s ON ms.skill_id = s.skill_id
            WHERE s.name IN ({placeholders})
            GROUP BY c.career_id, c.title, c.description
            ORDER BY skill_matches DESC, c.title
        """, skills)
        
        careers = []
        for row in cursor.fetchall():
            careers.append({
                'career_id': row[0],
                'title': row[1],
                'description': row[2],
                'skill_matches': row[3]
            })
        
        conn.close()
        return careers

# Example usage functions
def print_career_roadmap(career_title: str):
    """Print a complete roadmap for a career"""
    db = DatabaseManager()
    
    # Find the career
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT career_id FROM careers WHERE title = ?", (career_title,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"Career '{career_title}' not found.")
        return
    
    career_id = result[0]
    roadmap = db.get_career_roadmap(career_id)
    
    print(f"\n=== {career_title} Roadmap ===\n")
    for milestone in roadmap:
        print(f"{milestone['order']}. {milestone['title']}")
        print("   Skills to learn:")
        for skill in milestone['skills']:
            print(f"   - {skill}")
        print()

if __name__ == "__main__":
    # Example: Print roadmap for Frontend Developer
    print_career_roadmap("Frontend Developer")
