
import sqlite3
import os


db_path = os.path.join(os.path.dirname(__file__), '..', 'margen_ai.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Populating database with sample knowledge...")


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


skills_to_add = [
    
    ('HTML5 & CSS3',), ('JavaScript (ES6+)',), ('React',), ('Vue.js',), ('TypeScript',),
    ('Git',), ('API Integration',), ('Responsive Design',), ('CSS Frameworks',), ('Webpack',),
    

    ('Python',), ('Node.js',), ('Java',), ('C#',), ('SQL',), ('NoSQL',), ('REST APIs',),
    ('GraphQL',), ('Docker',), ('Microservices',), ('Database Design',), ('Authentication',),
    
    
    ('Python',), ('R',), ('SQL',), ('Machine Learning',), ('Statistics',), ('Data Visualization',),
    ('Pandas',), ('NumPy',), ('Scikit-learn',), ('TensorFlow',), ('Jupyter Notebooks',),
    
    
    ('Figma',), ('Adobe XD',), ('Sketch',), ('User Research',), ('Wireframing',), ('Prototyping',),
    ('Usability Testing',), ('Design Systems',), ('Typography',), ('Color Theory',),
    

    ('Linux',), ('Docker',), ('Kubernetes',), ('AWS',), ('Azure',), ('CI/CD',), ('Terraform',),
    ('Ansible',), ('Monitoring',), ('Logging',), ('Security',), ('Networking',)
]

cursor.executemany("INSERT OR IGNORE INTO skills (name) VALUES (?)", skills_to_add)


milestones_data = [
    
    (1, 1, "Foundational Knowledge", 1),
    (2, 1, "Framework Mastery", 2),
    (3, 1, "Advanced Concepts", 3),
    (4, 1, "Performance & Optimization", 4),
    
    
    (5, 2, "Programming Fundamentals", 1),
    (6, 2, "Database & APIs", 2),
    (7, 2, "Architecture & Design", 3),
    (8, 2, "DevOps & Deployment", 4),
    
    
    (9, 3, "Mathematics & Statistics", 1),
    (10, 3, "Programming & Data Manipulation", 2),
    (11, 3, "Machine Learning", 3),
    (12, 3, "Advanced Analytics", 4),
    
    
    (13, 4, "Design Fundamentals", 1),
    (14, 4, "User Research", 2),
    (15, 4, "Prototyping & Testing", 3),
    (16, 4, "Design Systems", 4),
    
    
    (17, 5, "Linux & Networking", 1),
    (18, 5, "Cloud Platforms", 2),
    (19, 5, "Containerization", 3),
    (20, 5, "Automation & CI/CD", 4)
]

cursor.executemany(
    "INSERT INTO milestones (milestone_id, career_id, title, milestone_order) VALUES (?, ?, ?, ?)",
    milestones_data
)


milestone_skills_data = [
    
    (1, 1), (1, 2), (1, 6), 
    
    
    (2, 3), (2, 4), (2, 5), (2, 7), 
    
    (3, 8), (3, 9), (3, 10),  
    
   
    (5, 12), (5, 13), (5, 14), (5, 6),  
    
    
    (6, 16), (6, 17), (6, 18), (6, 19),  
    
   
    (7, 20), (7, 21), (7, 22),  
    
   
    (9, 25), (9, 26), 
    
   
    (10, 12), (10, 16), (10, 27), (10, 28), 
    
    
    (11, 29), (11, 30), (11, 31),  
    
    
    (13, 33), (13, 34), (13, 35), (13, 39), (13, 40), 
    
    
    (14, 36), (14, 37),
    
   
    (15, 37), (15, 38),  
    
   
    (17, 42), (17, 52), 
    
   
    (18, 44), (18, 45),  
    
    
    (19, 43), (19, 46),  
    
    (20, 47), (20, 48), (20, 49), (20, 50), (20, 51)  
]


for milestone_id, skill_name_index in milestone_skills_data:
    
    skill_name = skills_to_add[skill_name_index - 1][0]
    cursor.execute(
        "INSERT INTO milestone_skills (milestone_id, skill_id) VALUES (?, (SELECT skill_id FROM skills WHERE name=?))",
        (milestone_id, skill_name)
    )

print("Sample data added successfully.")

conn.commit()
conn.close()

print(f"Database populated at: {db_path}")
