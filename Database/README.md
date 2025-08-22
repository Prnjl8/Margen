# Career Advisor Database System

A comprehensive career guidance system with a SQLite database backend, Flask API, and React frontend. This system helps users explore careers, manage their skills and interests, and follow structured learning paths.

## 🚀 Features

### Database Features
- **User Management**: Store user profiles with skills and interests
- **Career Database**: Comprehensive career information and requirements
- **Skills Library**: Extensive collection of skills with descriptions
- **Learning Roadmaps**: Structured learning paths for career development
- **Resource Management**: Curated learning resources for each skill

### Frontend Features
- **Modern UI**: Beautiful Material-UI based interface
- **Dashboard**: Overview with statistics and charts
- **User Management**: Add, edit, and delete user profiles
- **Career Browser**: Explore career paths and requirements
- **Skills Library**: Searchable skills with difficulty levels
- **Learning Resources**: Access curated learning materials
- **Career Roadmaps**: Interactive learning paths
- **Responsive Design**: Works on all devices

### Backend Features
- **RESTful API**: Complete API for all database operations
- **Career Matching**: Intelligent career recommendations
- **Data Analytics**: Statistics and insights
- **CORS Support**: Cross-origin resource sharing enabled

## 📁 Project Structure

```
Database/
├── advisor.db              # SQLite database file
├── creat.db.py            # Database creation script
├── populate_db.py         # Sample data population script
├── backend/
│   ├── app.py             # Flask API server
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html     # Main HTML file
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── App.js         # Main app component
│   │   └── index.js       # App entry point
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm or yarn

### 1. Database Setup

First, set up the database:

```bash
cd Database

# Create the database and tables
python creat.db.py

# Populate with sample data
python populate_db.py
```

### 2. Backend Setup

Set up the Flask API server:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Frontend Setup

Set up the React frontend:

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🗄️ Database Schema

### Tables

1. **users** - User profiles
   - user_id (PRIMARY KEY)
   - username (UNIQUE)

2. **user_interests** - User interests
   - interest_id (PRIMARY KEY)
   - user_id (FOREIGN KEY)
   - interest_name

3. **user_skills** - User skills
   - entry_id (PRIMARY KEY)
   - user_id (FOREIGN KEY)
   - skill_name

4. **careers** - Career information
   - career_id (PRIMARY KEY)
   - career_name (UNIQUE)
   - description

5. **skills** - Skills library
   - skill_id (PRIMARY KEY)
   - skill_name (UNIQUE)
   - description

6. **roadmap_steps** - Learning path steps
   - step_id (PRIMARY KEY)
   - career_id (FOREIGN KEY)
   - skill_id (FOREIGN KEY)
   - stage (Beginner/Intermediate/Advanced)
   - stage_order

7. **resources** - Learning resources
   - resource_id (PRIMARY KEY)
   - skill_id (FOREIGN KEY)
   - resource_type (Video/Course/Article/Website)
   - title
   - url

## 🔌 API Endpoints

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Create new user

### Careers
- `GET /api/careers` - Get all careers

### Skills
- `GET /api/skills` - Get all skills

### Roadmaps
- `GET /api/roadmaps` - Get all learning roadmaps

### Resources
- `GET /api/resources` - Get all learning resources

### Recommendations
- `GET /api/recommendations/<user_id>` - Get career recommendations for user

### Statistics
- `GET /api/stats` - Get dashboard statistics

## 🎨 Frontend Pages

### Dashboard (`/`)
- Overview statistics
- Recent user activity
- Skills distribution charts
- Interactive visualizations

### Users (`/users`)
- User profile management
- Add/edit/delete users
- View skills and interests
- User statistics

### Careers (`/careers`)
- Browse career paths
- View requirements
- Career details and descriptions

### Skills (`/skills`)
- Searchable skills library
- Difficulty levels
- Skill descriptions
- Filtering options

### Resources (`/resources`)
- Learning materials by skill
- Resource categorization
- Direct links to external content

### Roadmaps (`/roadmaps`)
- Structured learning paths
- Step-by-step progression
- Prerequisites and timelines

## 🔧 Configuration

### Backend Configuration
- Database path: Set in `backend/app.py`
- API port: Default 5000
- CORS: Enabled for frontend integration

### Frontend Configuration
- API URL: Set in `frontend/src/services/api.js`
- Default: `http://localhost:5000/api`
- Fallback to mock data if API unavailable

## 🚀 Deployment

### Production Build

1. **Backend Deployment**:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Use gunicorn or uwsgi for production
   gunicorn app:app
   ```

2. **Frontend Deployment**:
   ```bash
   cd frontend
   npm run build
   # Deploy the 'build' folder to your web server
   ```

### Environment Variables
- Set `FLASK_ENV=production` for backend
- Update API URL in frontend for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with details

## 🔮 Future Enhancements

- User authentication and authorization
- Advanced career matching algorithms
- Progress tracking for learning paths
- Social features and user communities
- Integration with external learning platforms
- Mobile app development
- Advanced analytics and reporting
