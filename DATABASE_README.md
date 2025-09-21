# MARGEN AI - Database Implementation

## Overview

This document describes the comprehensive SQLite database implementation for the MARGEN AI Career Advisor application. The database provides persistent storage for all user data, AI interactions, and learning progress.

## Database Schema

### Core Tables

#### 1. User Management
- **`users`** - User accounts with authentication
- **`otps`** - OTP verification codes for phone verification

#### 2. Skills and Interests
- **`skills`** - Master skills database
- **`user_skills`** - User skills with proficiency levels
- **`interests`** - Master interests database  
- **`user_interests`** - User interests with intensity levels

#### 3. Career and Recommendations
- **`careers`** - Master careers database
- **`career_skills`** - Skills required for careers
- **`career_recommendations`** - AI-generated career recommendations

#### 4. Learning and Progress
- **`roadmaps`** - Learning roadmaps for careers
- **`roadmap_skills`** - Skills within roadmaps
- **`user_progress`** - User progress tracking
- **`learning_sessions`** - Learning session tracking

#### 5. AI and Analytics
- **`ai_interactions`** - Track AI interactions and responses
- **`user_analytics`** - User behavior and analytics

## Key Features

### 🔐 User Authentication
- Email/password registration and login
- Phone number verification with OTP
- Password hashing with Werkzeug
- User profile management

### 🎯 Skills Management
- Comprehensive skills database (technical, soft, domain)
- User skill proficiency tracking (beginner to expert)
- Confidence scoring (1-10 scale)
- Experience tracking and project counts
- Certification management

### 🚀 Career Recommendations
- AI-powered career matching using Gemini
- Match percentage and confidence scoring
- Skill gap analysis
- Learning priority assessment
- Persistent recommendation storage

### 📊 Analytics
- User behavior tracking
- AI interaction logging
- Learning progress monitoring
- Performance analytics

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r backend/requirements_with_database.txt
```

### 2. Initialize Database
```bash
python init_database.py
```

### 3. Run Application
```bash
python backend/app_with_database.py
```

## Database Models

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_completed = db.Column(db.Boolean, default=False)
```

### Skills Model
```python
class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    proficiency_level = db.Column(db.String(20))  # beginner, intermediate, advanced, expert
    confidence_score = db.Column(db.Integer)  # 1-10 scale
    years_experience = db.Column(db.Float, default=0.0)
    last_practiced = db.Column(db.DateTime, nullable=True)
    projects_count = db.Column(db.Integer, default=0)
    certifications = db.Column(db.Text)  # JSON string
    is_verified = db.Column(db.Boolean, default=False)
```

## API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /signin` - User login
- `POST /send-otp` - Send OTP to phone
- `POST /verify-otp` - Verify OTP code

### User Profile
- `GET /user-profile` - Get user profile with skills/interests
- `POST /update-skills` - Update user skills
- `POST /update-interests` - Update user interests

### AI Features
- `POST /generate-careers` - Generate AI career recommendations
- `GET /get-user-recommendations` - Get user's career recommendations
- `POST /generate-roadmap` - Create learning roadmap for career

### Analytics
- `GET /user-analytics` - Get user analytics data
- `GET /database/status` - Get database status
- `POST /database/reset` - Reset database (development)

## Database Relationships

### User Relationships
```
User (1) ──→ (Many) UserSkill
User (1) ──→ (Many) UserInterest  
User (1) ──→ (Many) CareerRecommendation
User (1) ──→ (Many) UserProgress
User (1) ──→ (Many) LearningSession
```

### Career Relationships
```
Career (1) ──→ (Many) CareerSkill
Career (1) ──→ (Many) CareerRecommendation
Career (1) ──→ (Many) Roadmap
```

### Skills Relationships
```
Skill (1) ──→ (Many) UserSkill
Skill (1) ──→ (Many) CareerSkill
Skill (1) ──→ (Many) RoadmapSkill
```

## Data Flow

### 1. User Registration
1. User signs up with email/password
2. User data stored in `users` table
3. Phone verification via OTP
4. User profile completion

### 2. Skills Assessment
1. User inputs skills and proficiency levels
2. Skills stored in `user_skills` table
3. Skills linked to master `skills` table
4. Confidence scores and experience tracked

### 3. Career Generation
1. AI analyzes user skills and interests
2. Generates personalized career recommendations
3. Recommendations stored in `career_recommendations` table
4. Match percentages and confidence scores saved

### 4. Learning Progress
1. User follows learning roadmaps
2. Progress tracked in `user_progress` table
3. Learning sessions logged in `learning_sessions` table
4. Analytics data collected for insights

## Security Features

### Password Security
- Passwords hashed using Werkzeug's security functions
- No plain text password storage
- Secure password verification

### Data Protection
- User data encrypted in transit
- Sensitive information properly handled
- OTP codes expire after 10 minutes
- Single-use OTP verification

### API Security
- Input validation on all endpoints
- SQL injection prevention via ORM
- CORS configuration for frontend
- Error handling without data exposure

## Performance Optimizations

### Database Indexing
- Email and phone number indexes for fast lookups
- User ID indexes for relationship queries
- Created_at indexes for time-based queries

### Query Optimization
- Efficient relationship loading
- Batch operations for bulk updates
- Pagination for large datasets
- Caching for frequently accessed data

## Monitoring and Analytics

### AI Interaction Tracking
- All AI requests logged with timestamps
- Response times and token usage tracked
- User satisfaction ratings collected
- Model performance monitoring

### User Analytics
- Page views and feature usage tracked
- Learning progress analytics
- Career recommendation effectiveness
- User engagement metrics

## Backup and Maintenance

### Database Backup
```bash
# Create backup
cp margen_ai.db margen_ai_backup_$(date +%Y%m%d).db

# Restore backup
cp margen_ai_backup_20240101.db margen_ai.db
```

### Data Cleanup
- OTP codes automatically expire
- Old analytics data can be archived
- User data retention policies
- Regular database maintenance

## Development Tools

### Database Browser
- Use SQLite Browser for visual database inspection
- View tables, relationships, and data
- Run custom queries for debugging

### Database Reset
```bash
# Reset database (development only)
curl -X POST http://localhost:5001/database/reset
```

### Status Check
```bash
# Check database status
curl http://localhost:5001/database/status
```

## Production Considerations

### Database Scaling
- Consider PostgreSQL for production
- Connection pooling for high traffic
- Read replicas for analytics queries
- Database sharding for large datasets

### Security Hardening
- Environment variable configuration
- API key rotation
- Rate limiting implementation
- Input sanitization

### Monitoring
- Database performance monitoring
- Query optimization
- Error tracking and alerting
- Backup automation

## Troubleshooting

### Common Issues
1. **Database locked**: Check for concurrent access
2. **Migration errors**: Verify table schemas
3. **Performance issues**: Check indexes and queries
4. **Data corruption**: Restore from backup

### Debug Commands
```python
# Check database connection
from database_models import db
print(db.engine.url)

# List all tables
print(db.metadata.tables.keys())

# Check table row counts
for table in db.metadata.tables:
    count = db.session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
    print(f"{table}: {count} rows")
```

## Conclusion

The MARGEN AI database implementation provides a robust foundation for the career advisory application with:

- ✅ Complete user management system
- ✅ Comprehensive skills and interests tracking  
- ✅ AI-powered career recommendations
- ✅ Learning progress monitoring
- ✅ Analytics and reporting
- ✅ Security and performance optimizations

This database schema supports all current features while being extensible for future enhancements.
