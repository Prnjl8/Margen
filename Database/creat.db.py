# create_db.py
import sqlite3
import os

# Get the path to the database file (one level up from Database directory)
db_path = os.path.join(os.path.dirname(__file__), '..', 'margen_ai.db')

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Database connected. Creating tables...")

# Drop existing tables to start fresh (optional)
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS user_profiles;")
cursor.execute("DROP TABLE IF EXISTS careers;")
cursor.execute("DROP TABLE IF EXISTS milestones;")
cursor.execute("DROP TABLE IF EXISTS skills;")
cursor.execute("DROP TABLE IF EXISTS milestone_skills;")


# --- Create User Profile Tables ---
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    phone_number TEXT UNIQUE,
    education_level TEXT
);
''')

cursor.execute('''
CREATE TABLE user_profiles (
    profile_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    interests TEXT,
    skills TEXT,
    aptitudes TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
''')

# --- Create Knowledge Base Tables ---
cursor.execute('''
CREATE TABLE careers (
    career_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE milestones (
    milestone_id INTEGER PRIMARY KEY,
    career_id INTEGER,
    title TEXT NOT NULL,
    milestone_order INTEGER NOT NULL,
    FOREIGN KEY (career_id) REFERENCES careers (career_id)
);
''')

cursor.execute('''
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
''')

cursor.execute('''
CREATE TABLE milestone_skills (
    milestone_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (milestone_id) REFERENCES milestones (milestone_id),
    FOREIGN KEY (skill_id) REFERENCES skills (skill_id),
    PRIMARY KEY (milestone_id, skill_id)
);
''')

print("All tables created successfully.")

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database created at: {db_path}")
