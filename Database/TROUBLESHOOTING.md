# Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the Career Advisor Database System.

## 🚨 Common Issues and Solutions

### 1. npm install vulnerabilities

**Problem**: You see warnings about vulnerabilities when running `npm install`

**Solution**:
```bash
# Clean install with updated packages
cd frontend
rm -rf node_modules package-lock.json
npm install

# If vulnerabilities persist, you can audit and fix them
npm audit fix
npm audit fix --force  # Only if necessary
```

### 2. Backend files missing

**Problem**: The backend folder or files are missing

**Solution**:
```bash
# Recreate backend folder structure
mkdir -p backend
cd backend

# Create requirements.txt
echo "Flask==2.3.3
Flask-CORS==4.0.0" > requirements.txt

# Install dependencies
pip install -r requirements.txt
```

### 3. Database not found

**Problem**: The application can't find the database file

**Solution**:
```bash
# Run the setup script
python setup.py

# Or manually create the database
python creat.db.py
python populate_db.py
```

### 4. Backend server won't start

**Problem**: Flask server fails to start

**Solutions**:

**Port already in use**:
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python app.py --port 5001
```

**Missing dependencies**:
```bash
pip install Flask Flask-CORS
```

**Permission issues**:
```bash
# On Windows, run as administrator
# On Linux/Mac, check file permissions
chmod +x app.py
```

### 5. Frontend can't connect to backend

**Problem**: Frontend shows "API call failed" messages

**Solutions**:

**Backend not running**:
```bash
# Start the backend first
cd backend
python app.py
```

**CORS issues**:
- Make sure Flask-CORS is installed
- Check that the backend is running on the correct port

**Wrong API URL**:
- Verify the API URL in `frontend/src/services/api.js`
- Default should be `http://localhost:5000/api`

### 6. React app won't start

**Problem**: `npm start` fails

**Solutions**:

**Port 3000 in use**:
```bash
# Use a different port
PORT=3001 npm start
```

**Node modules corrupted**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Outdated Node.js**:
```bash
# Check Node.js version (should be 14+)
node --version

# Update Node.js if needed
```

### 7. Database connection errors

**Problem**: Backend can't connect to the database

**Solutions**:

**Database file permissions**:
```bash
# Check file permissions
ls -la advisor.db

# Fix permissions if needed
chmod 644 advisor.db
```

**Database corrupted**:
```bash
# Recreate the database
rm advisor.db
python creat.db.py
python populate_db.py
```

**SQLite not available**:
```bash
# Install SQLite if missing
# On Ubuntu/Debian:
sudo apt-get install sqlite3

# On macOS:
brew install sqlite3

# On Windows, SQLite should be included with Python
```

## 🔧 Quick Fix Commands

### Complete Reset
```bash
# Stop all running processes
pkill -f "python app.py"
pkill -f "npm start"

# Clean everything
rm -rf frontend/node_modules frontend/package-lock.json
rm -f advisor.db

# Reinstall everything
python setup.py
cd frontend && npm install
```

### Check System Status
```bash
# Check if backend is running
curl http://localhost:5000/api/stats

# Check if frontend is running
curl http://localhost:3000

# Check database
sqlite3 advisor.db "SELECT COUNT(*) FROM users;"
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **Node.js**: 14 or higher
- **npm**: 6 or higher
- **SQLite**: 3.0 or higher

### Recommended
- **Python**: 3.9 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **RAM**: 4GB or more
- **Storage**: 1GB free space

## 🆘 Getting Help

If you're still having issues:

1. **Check the logs**:
   - Backend: Look at the terminal where you ran `python app.py`
   - Frontend: Check the browser console (F12)

2. **Verify your setup**:
   ```bash
   python setup.py
   ```

3. **Test individual components**:
   ```bash
   # Test backend
   cd backend && python app.py
   
   # Test frontend (in new terminal)
   cd frontend && npm start
   ```

4. **Common error messages**:
   - `ModuleNotFoundError`: Install missing Python packages
   - `EADDRINUSE`: Port is already in use
   - `ENOENT`: File or directory not found
   - `CORS error`: Backend not running or CORS not configured

## 🎯 Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Node.js 14+ installed
- [ ] Database created (`python setup.py`)
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running (`python app.py`)
- [ ] Frontend running (`npm start`)
- [ ] Browser opened to `http://localhost:3000`
