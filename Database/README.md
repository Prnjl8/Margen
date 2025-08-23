# Database Setup for AI Career Advisor

This directory contains the database setup scripts for the AI Career Advisor application.

## Database Structure

The application uses SQLite with the following tables:

### User Profile Data
- **users**: Core login and profile information
- **user_profiles**: User interests, skills, and aptitudes

### Knowledge Base
- **careers**: Career options and descriptions
- **milestones**: Roadmap steps for each career
- **skills**: Master list of all possible skills
- **milestone_skills**: Links skills to milestones

## Setup Instructions

### Step 1: Create the Database Structure
Run the database creation script to set up all tables:

```bash
cd Database
python create_db.py
```

This will create a `margen_ai.db` file in the parent directory with all the necessary tables.

### Step 2: Populate with Sample Data (Optional)
Add sample career and roadmap data to make the database immediately useful:

```bash
python populate_db.py
```

This adds:
- 5 sample careers (Frontend Developer, Backend Developer, Data Scientist, UX/UI Designer, DevOps Engineer)
- 52 skills across different domains
- 20 milestones (4 per career)
- Skill-milestone relationships

## Database Schema

### users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    phone_number TEXT UNIQUE,
    education_level TEXT
);
```

### user_profiles Table
```sql
CREATE TABLE user_profiles (
    profile_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    interests TEXT,
    skills TEXT,
    aptitudes TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

### careers Table
```sql
CREATE TABLE careers (
    career_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);
```

### milestones Table
```sql
CREATE TABLE milestones (
    milestone_id INTEGER PRIMARY KEY,
    career_id INTEGER,
    title TEXT NOT NULL,
    milestone_order INTEGER NOT NULL,
    FOREIGN KEY (career_id) REFERENCES careers (career_id)
);
```

### skills Table
```sql
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
```

### milestone_skills Table
```sql
CREATE TABLE milestone_skills (
    milestone_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (milestone_id) REFERENCES milestones (milestone_id),
    FOREIGN KEY (skill_id) REFERENCES skills (skill_id),
    PRIMARY KEY (milestone_id, skill_id)
);
```

## Usage Notes

- The database file (`margen_ai.db`) will be created in the parent directory
- The `create_db.py` script drops existing tables to start fresh
- The `populate_db.py` script uses `INSERT OR IGNORE` to avoid duplicate skills
- All foreign key relationships are properly maintained
- The milestone_order field ensures milestones are displayed in the correct sequence

## Next Steps

Once the database is set up, your backend developer can:
1. Connect to the database using the path: `../margen_ai.db`
2. Query careers, milestones, and skills for the AI recommendations
3. Store user data from the authentication and profile forms
4. Build the AI logic to match user profiles with career recommendations
