# populate_db.py
import sqlite3
import os

# Get the path to the database file (one level up from Database directory)
db_path = os.path.join(os.path.dirname(__file__), '..', 'margen_ai.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Populating database with sample knowledge...")

# Add sample careers
careers_to_add = [
    (1, "Frontend Developer", "Build beautiful, responsive, and user-friendly websites and web applications."),
    (2, "Backend Developer", "Develop server-side logic, databases, and APIs that power web applications."),
    (3, "Data Scientist", "Analyze complex data sets to help organizations make better decisions."),
    (4, "UX/UI Designer", "Create intuitive and engaging user experiences through design and research."),
    (5, "DevOps Engineer", "Bridge the gap between development and operations through automation and infrastructure management.")
]

cursor.executemany(
    "INSERT INTO careers (career_id, title, description) VALUES (?, ?, ?)",
    careers_to_add
)

# Add skills for these careers
skills_to_add = [
    # Frontend skills
    ('HTML5 & CSS3',), ('JavaScript (ES6+)',), ('React',), ('Vue.js',), ('TypeScript',),
    ('Git',), ('API Integration',), ('Responsive Design',), ('CSS Frameworks',), ('Webpack',),
    
    # Backend skills
    ('Python',), ('Node.js',), ('Java',), ('C#',), ('SQL',), ('NoSQL',), ('REST APIs',),
    ('GraphQL',), ('Docker',), ('Microservices',), ('Database Design',), ('Authentication',),
    
    # Data Science skills
    ('Python',), ('R',), ('SQL',), ('Machine Learning',), ('Statistics',), ('Data Visualization',),
    ('Pandas',), ('NumPy',), ('Scikit-learn',), ('TensorFlow',), ('Jupyter Notebooks',),
    
    # UX/UI skills
    ('Figma',), ('Adobe XD',), ('Sketch',), ('User Research',), ('Wireframing',), ('Prototyping',),
    ('Usability Testing',), ('Design Systems',), ('Typography',), ('Color Theory',),
    
    # DevOps skills
    ('Linux',), ('Docker',), ('Kubernetes',), ('AWS',), ('Azure',), ('CI/CD',), ('Terraform',),
    ('Ansible',), ('Monitoring',), ('Logging',), ('Security',), ('Networking',)
]

cursor.executemany("INSERT OR IGNORE INTO skills (name) VALUES (?)", skills_to_add)

# Add milestones for each career
milestones_data = [
    # Frontend Developer milestones
    (1, 1, "Foundational Knowledge", 1),
    (2, 1, "Framework Mastery", 2),
    (3, 1, "Advanced Concepts", 3),
    (4, 1, "Performance & Optimization", 4),
    
    # Backend Developer milestones
    (5, 2, "Programming Fundamentals", 1),
    (6, 2, "Database & APIs", 2),
    (7, 2, "Architecture & Design", 3),
    (8, 2, "DevOps & Deployment", 4),
    
    # Data Scientist milestones
    (9, 3, "Mathematics & Statistics", 1),
    (10, 3, "Programming & Data Manipulation", 2),
    (11, 3, "Machine Learning", 3),
    (12, 3, "Advanced Analytics", 4),
    
    # UX/UI Designer milestones
    (13, 4, "Design Fundamentals", 1),
    (14, 4, "User Research", 2),
    (15, 4, "Prototyping & Testing", 3),
    (16, 4, "Design Systems", 4),
    
    # DevOps Engineer milestones
    (17, 5, "Linux & Networking", 1),
    (18, 5, "Cloud Platforms", 2),
    (19, 5, "Containerization", 3),
    (20, 5, "Automation & CI/CD", 4)
]

cursor.executemany(
    "INSERT INTO milestones (milestone_id, career_id, title, milestone_order) VALUES (?, ?, ?, ?)",
    milestones_data
)

# Link skills to milestones
milestone_skills_data = [
    # Frontend Developer - Foundational Knowledge
    (1, 1), (1, 2), (1, 6),  # HTML5 & CSS3, JavaScript, Git
    
    # Frontend Developer - Framework Mastery
    (2, 3), (2, 4), (2, 5), (2, 7),  # React, Vue.js, TypeScript, API Integration
    
    # Frontend Developer - Advanced Concepts
    (3, 8), (3, 9), (3, 10),  # Responsive Design, CSS Frameworks, Webpack
    
    # Backend Developer - Programming Fundamentals
    (5, 12), (5, 13), (5, 14), (5, 6),  # Python, Node.js, Java, Git
    
    # Backend Developer - Database & APIs
    (6, 16), (6, 17), (6, 18), (6, 19),  # SQL, NoSQL, REST APIs, GraphQL
    
    # Backend Developer - Architecture & Design
    (7, 20), (7, 21), (7, 22),  # Microservices, Database Design, Authentication
    
    # Data Scientist - Mathematics & Statistics
    (9, 25), (9, 26),  # Statistics, Data Visualization
    
    # Data Scientist - Programming & Data Manipulation
    (10, 12), (10, 16), (10, 27), (10, 28),  # Python, SQL, Pandas, NumPy
    
    # Data Scientist - Machine Learning
    (11, 29), (11, 30), (11, 31),  # Machine Learning, Scikit-learn, TensorFlow
    
    # UX/UI Designer - Design Fundamentals
    (13, 33), (13, 34), (13, 35), (13, 39), (13, 40),  # Figma, Adobe XD, Sketch, Typography, Color Theory
    
    # UX/UI Designer - User Research
    (14, 36), (14, 37),  # User Research, Usability Testing
    
    # UX/UI Designer - Prototyping & Testing
    (15, 37), (15, 38),  # Usability Testing, Wireframing, Prototyping
    
    # DevOps Engineer - Linux & Networking
    (17, 42), (17, 52),  # Linux, Networking
    
    # DevOps Engineer - Cloud Platforms
    (18, 44), (18, 45),  # AWS, Azure
    
    # DevOps Engineer - Containerization
    (19, 43), (19, 46),  # Docker, Kubernetes
    
    # DevOps Engineer - Automation & CI/CD
    (20, 47), (20, 48), (20, 49), (20, 50), (20, 51)  # CI/CD, Terraform, Ansible, Monitoring, Logging, Security
]

# Get skill IDs and create milestone_skills entries
for milestone_id, skill_name_index in milestone_skills_data:
    # skill_name_index is 1-based index into the skills_to_add list
    skill_name = skills_to_add[skill_name_index - 1][0]
    cursor.execute(
        "INSERT INTO milestone_skills (milestone_id, skill_id) VALUES (?, (SELECT skill_id FROM skills WHERE name=?))",
        (milestone_id, skill_name)
    )

print("Sample data added successfully.")

conn.commit()
conn.close()

print(f"Database populated at: {db_path}")
