# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11+
- Git

### Step 1: Clone & Setup (1 min)

```bash
# Clone repository
git clone https://github.com/yourusername/jwt-auth-app.git
cd jwt-auth-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Backend (1 min)

```bash
# Terminal 1
cd backend
python app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
```

### Step 3: Start Frontend (1 min)

```bash
# Terminal 2
cd frontend
python -m http.server 3000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 3000
```

### Step 4: Open Application (1 min)

Visit: **http://localhost:3000**

### Step 5: Test It! (1 min)

1. **Register a new account:**
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `TestPassword123` (min 8 chars)
   - Confirm: `TestPassword123`
   - Click "Register"

2. **Or Login:**
   - Click "Already have an account? Login"
   - Enter credentials
   - Click "Login"

3. **Logout:**
   - Click "Logout" button

---

## 🐳 Docker Quick Start

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

Access at: **http://localhost:5000** (API) / **http://localhost:3000** (Frontend)

---

## 🧪 Run Tests

```bash
# Install test dependencies (if not done)
pip install pytest playwright

# Install browser
playwright install chromium

# Run all tests
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::TestRegistration::test_register_with_valid_data -v
```

---

## 📝 Common Tasks

### Reset Database
```bash
rm backend/users.db
# Restart the backend
```

### Change API Port
```bash
# In backend/app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### View Database (SQLite)

```bash
sqlite3 backend/users.db
> .tables
> SELECT * FROM users;
> .quit
```

### Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
# Edit .env with your settings
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Mac/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Won't Run
```bash
# Install Playwright browsers
playwright install chromium

# Make sure services are running
# Terminal 1: python backend/app.py
# Terminal 2: python -m http.server 3000
```

### CORS Errors
- Frontend and backend must be running
- Backend runs on port 5000 (http://localhost:5000)
- Frontend runs on port 3000 (http://localhost:3000)

---

## 📚 Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Review Code Structure**: Check project folders
3. **Explore API**: Use curl or Postman
4. **Run Tests**: Execute E2E tests
5. **Modify & Extend**: Add your own features

---

## 💡 Tips

- **API Testing**: `curl -X POST http://localhost:5000/login -d '{"email":"test@example.com","password":"TestPassword123"}' -H "Content-Type: application/json"`
- **View Network Requests**: Use browser DevTools (F12)
- **Frontend Changes**: Just refresh browser (no restart needed)
- **Backend Changes**: Restart `python app.py`
- **Database Changes**: Delete `users.db` and restart

---

## 🎯 What to Explore

- **Frontend**: Check `frontend/script.js` for validation logic
- **Backend**: Check `backend/app.py` for route handlers
- **Tests**: Check `tests/test_auth.py` for test examples
- **CI/CD**: Check `.github/workflows/ci-cd.yml` for automation

---

**Need help?** Check README.md for comprehensive documentation or open an issue on GitHub.

Happy coding! 🚀
