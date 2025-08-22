# populate_db.py
import sqlite3

conn = sqlite3.connect('advisor.db')
cursor = conn.cursor()

print("Connected to the database.")

# --- POPULATE USER DATA (Sample Users) ---

# Clear existing user data to avoid duplicates when re-running
cursor.execute("DELETE FROM users;")
cursor.execute("DELETE FROM user_interests;")
cursor.execute("DELETE FROM user_skills;")

# Create User 1: Priya
cursor.execute("INSERT INTO users (user_id, username) VALUES (1, 'Priya');")
cursor.execute("INSERT INTO user_interests (user_id, interest_name) VALUES (1, 'Data Analysis');")
cursor.execute("INSERT INTO user_interests (user_id, interest_name) VALUES (1, 'Business');")
cursor.execute("INSERT INTO user_skills (user_id, skill_name) VALUES (1, 'SQL');")
cursor.execute("INSERT INTO user_skills (user_id, skill_name) VALUES (1, 'Excel');")

# Create User 2: Alex
cursor.execute("INSERT INTO users (user_id, username) VALUES (2, 'Alex');")
cursor.execute("INSERT INTO user_interests (user_id, interest_name) VALUES (2, 'Web Design');")
cursor.execute("INSERT INTO user_interests (user_id, interest_name) VALUES (2, 'Art');")
cursor.execute("INSERT INTO user_skills (user_id, skill_name) VALUES (2, 'HTML');")

print("Sample user data populated.")

# --- POPULATE KNOWLEDGE BASE (for Data Analyst career) ---

# Clear existing knowledge data
cursor.execute("DELETE FROM careers;")
cursor.execute("DELETE FROM skills;")
cursor.execute("DELETE FROM roadmap_steps;")
cursor.execute("DELETE FROM resources;")

# Populate Careers
cursor.execute("INSERT INTO careers (career_id, career_name, description) VALUES (101, 'Data Analyst', 'Data analysts collect, clean, and interpret data sets to answer a question or solve a problem.');")

# Populate Skills for Data Analyst
skills_to_add = [
    (1, 'SQL', 'The language for managing data in relational databases.'),
    (2, 'Python', 'A versatile programming language with powerful data analysis libraries.'),
    (3, 'Tableau', 'A popular data visualization tool.'),
    (4, 'Statistics', 'The science of collecting, analyzing, and interpreting data.')
]
cursor.executemany("INSERT INTO skills (skill_id, skill_name, description) VALUES (?, ?, ?);", skills_to_add)

# Populate Roadmap Steps for Data Analyst (Career ID 101)
roadmap_steps_to_add = [
    (101, 4, 'Beginner', 1), # Data Analyst, Statistics, Beginner, Order 1
    (101, 1, 'Beginner', 2), # Data Analyst, SQL, Beginner, Order 2
    (101, 2, 'Intermediate', 1), # Data Analyst, Python, Intermediate, Order 1
    (101, 3, 'Intermediate', 2)  # Data Analyst, Tableau, Intermediate, Order 2
]
cursor.executemany("INSERT INTO roadmap_steps (career_id, skill_id, stage, stage_order) VALUES (?, ?, ?, ?);", roadmap_steps_to_add)

# Populate Resources for some skills
resources_to_add = [
    (1, 'Course', 'Khan Academy - SQL: Querying and managing data', 'https://www.khanacademy.org/computing/computer-programming/sql'),
    (1, 'Video', 'SQL for Beginners by freeCodeCamp', 'https://www.youtube.com/watch?v=HXV3zeQKqGY'),
    (2, 'Course', 'Python for Everybody (Coursera)', 'https://www.coursera.org/specializations/python'),
    (3, 'Website', 'Tableau Public - Free Training Videos', 'https://public.tableau.com/en-us/s/resources')
]
cursor.executemany("INSERT INTO resources (skill_id, resource_type, title, url) VALUES (?, ?, ?, ?);", resources_to_add)

print("Knowledge base for Data Analyst populated.")

# Commit changes and close
conn.commit()
conn.close()

print("Data population complete. Database is ready.")