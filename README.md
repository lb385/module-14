# JWT Authentication Application

A modern, full-stack authentication application with JWT-based login and registration, complete with E2E testing and CI/CD pipeline.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Frontend](#frontend)
- [E2E Tests](#e2e-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Documentation](#api-documentation)
- [Docker Hub Repository](#docker-hub-repository)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Backend
- **JWT Authentication**: Secure token-based authentication
- **User Registration**: Create new user accounts with validation
- **User Login**: Authenticate users and issue JWT tokens
- **Password Hashing**: Secure password storage using werkzeug
- **Pydantic Validation**: Strong data validation for all requests
- **CORS Support**: Allow frontend communication across origins
- **BREAD Calculation Endpoints**: 
  - Browse: GET /calculations - Retrieve all user calculations
  - Read: GET /calculations/{id} - Get specific calculation details
  - Edit: PATCH /calculations/{id} - Update calculations
  - Add: POST /calculations - Create new calculations
  - Delete: DELETE /calculations/{id} - Remove calculations
- **Automatic Calculation**: Supports add, subtract, multiply, and divide operations

### Frontend
- **Registration Page**: User-friendly registration form with validation
- **Login Page**: Simple login interface
- **Dashboard**: Main application interface after authentication
- **Calculation Management**: 
  - Create calculations with form validation
  - Browse and display all calculations in a grid layout
  - View calculation details in a modal
  - Edit calculations with partial updates
  - Delete calculations with confirmation
- **Client-side Validation**: Email format, password requirements, numeric checks
- **Token Storage**: Secure JWT token handling in localStorage
- **Responsive Design**: Works on desktop and mobile devices

### Testing
- **Positive Tests**: Validate successful registration and login
- **Negative Tests**: Handle invalid inputs gracefully
- **Form Validation**: Test both client-side and server-side validation
- **Token Handling**: Verify token storage and clearance

### CI/CD
- **Automated Testing**: Run E2E tests on every commit
- **Docker Build**: Containerize the application
- **Docker Hub Integration**: Push images to Docker Hub
- **GitHub Actions**: Fully automated pipeline

## 🛠 Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **PyJWT**: JWT token generation and validation
- **Pydantic**: Data validation
- **PostgreSQL**: Database (in production)
- **SQLite**: Database (in development)

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: No frameworks for simplicity
- **LocalStorage API**: Token persistence

### Testing & Deployment
- **Playwright**: E2E testing framework
- **pytest**: Python testing framework
- **Docker**: Containerization
- **GitHub Actions**: CI/CD automation

## � Project Structure

```
module-13/
├── backend/
│   ├── app.py                 # Flask application and routes (including BREAD endpoints)
│   ├── models.py              # SQLAlchemy User and Calculation models
│   ├── schemas.py             # Pydantic validation schemas
│   ├── utils.py               # JWT utilities and decorators
│   └── config.py              # Configuration settings
├── frontend/
│   ├── index.html             # Main HTML page with calculation dashboard
│   ├── styles.css             # CSS styling (including calculation forms)
│   └── script.js              # JavaScript functionality (BREAD operations)
├── tests/
│   ├── test_auth.py           # E2E authentication tests
│   ├── test_calculations.py   # E2E calculation BREAD operation tests
│   └── conftest.py            # Pytest configuration
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── README.md                  # This file
├── BREAD_API_DOCUMENTATION.md # Detailed BREAD API documentation
└── REFLECTION.md              # Development reflection document
```

## 🔧 Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (optional, for containerization)
- **Git** (for version control)
- **Node.js 18+** (for frontend development, optional)
- **PostgreSQL 15** (for production, or SQLite for development)

## 💻 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jwt-auth-app.git
cd jwt-auth-app
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-jwt-key-change-in-production
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///users.db  # Or postgresql://user:pass@localhost/db
```

## 🚀 Running the Application

### Option 1: Using Python (Development)

#### Terminal 1 - Backend

```bash
cd backend
python app.py
```

The backend will start at `http://localhost:5000`

#### Terminal 2 - Frontend

```bash
cd frontend
python -m http.server 3000
```

The frontend will start at `http://localhost:3000`

### Option 2: Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database at `localhost:5432`
- Flask backend at `http://localhost:5000`
- Frontend accessible via Docker service

### Option 3: Using Docker

Build the image:

```bash
docker build -t jwt-auth-app .
```

Run the container:

```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/auth_db \
  -e JWT_SECRET_KEY=your-secret-key \
  jwt-auth-app
```

## 📱 Frontend

### Registration Page

Access at `http://localhost:3000`

**Features:**
- Email validation (RFC-compliant)
- Username field (3+ characters)
- Password field (8+ characters)
- Password confirmation
- Real-time client-side validation
- Success/error message display

**Fields:**
- `email`: Valid email address (required)
- `username`: 3-120 characters, alphanumeric + underscore (required)
- `password`: 8-255 characters (required)
- `confirm_password`: Must match password (required)

### Login Page

Click "Already have an account? Login" to access the login form

**Features:**
- Email validation
- Password validation
- Real-time feedback
- Persistent token storage

**Fields:**
- `email`: Valid email address (required)
- `password`: 8+ characters (required)

## 🧪 E2E Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Authentication Tests

```bash
pytest tests/test_auth.py -v
```

### Run Calculation BREAD Tests

```bash
pytest tests/test_calculations.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_calculations.py::TestCalculationCreate -v
```

### Run Specific Test

```bash
pytest tests/test_calculations.py::TestCalculationCreate::test_create_calculation_add_operation -v
```

### Test Coverage

Run with coverage report:

```bash
pip install pytest-cov
pytest tests/ --cov=backend --cov-report=html
```

### Test Categories

**Calculation Browse Tests:**
- ✅ Browse empty calculations list
- ✅ Browse displays multiple calculations

**Calculation Create (Add) Tests:**
- ✅ Create with valid data
- ✅ Create add operation
- ✅ Create subtract operation
- ✅ Create multiply operation
- ✅ Create divide operation
- ✅ Reject missing operation
- ✅ Reject invalid operand
- ✅ Reject division by zero
- ✅ Support decimal operands

**Calculation Read Tests:**
- ✅ Read single calculation
- ✅ Read calculation details

**Calculation Update (Edit) Tests:**
- ✅ Update operation
- ✅ Update operands
- ✅ Update all fields
- ✅ Reject empty update

**Calculation Delete Tests:**
- ✅ Delete single calculation
- ✅ Delete one of multiple calculations

**Security Tests:**
- ✅ Reject unauthorized access
- ✅ User data isolation
- ✅ Invalid ID handling

**Edge Case Tests:**
- ✅ Large numbers
- ✅ Negative numbers
- ✅ Zero operand
- ✅ Multiple sequential operations
- ✅ Decimal precision

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Located at `.github/workflows/ci-cd.yml`

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Steps:**

1. **Setup**: Checkout code, set up Python and Node.js
2. **Dependencies**: Install Python and Node.js packages
3. **Build Database**: Spin up PostgreSQL service
4. **Start Services**: Start backend and frontend
5. **Run Tests**: Execute E2E tests with Playwright
6. **Upload Reports**: Store test results as artifacts
7. **Build Docker Image**: Create Docker image
8. **Push to Docker Hub**: Deploy image to Docker Hub

### Environment Variables in GitHub

Set these secrets in your GitHub repository settings:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token
- `DATABASE_URL`: Production database URL (if needed)
- `JWT_SECRET_KEY`: Production JWT secret
- `SECRET_KEY`: Production Flask secret key

### Docker Hub Integration

The workflow automatically pushes images to Docker Hub when:
- Tests pass successfully
- Code is pushed to `main` or `develop` branches

Image tags:
- `latest`: Most recent build
- `{commit-sha}`: Specific commit version

## 📚 API Documentation

### BREAD Operations for Calculations

The application includes complete BREAD (Browse, Read, Edit, Add, Delete) endpoints for managing calculations.

#### Quick Reference

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| Browse | GET | /calculations | Get all user's calculations |
| Read | GET | /calculations/{id} | Get specific calculation |
| Add | POST | /calculations | Create new calculation |
| Edit | PATCH | /calculations/{id} | Update calculation |
| Delete | DELETE | /calculations/{id} | Delete calculation |

#### Operations Supported

- **add**: Addition (operand1 + operand2)
- **subtract**: Subtraction (operand1 - operand2)
- **multiply**: Multiplication (operand1 × operand2)
- **divide**: Division (operand1 ÷ operand2)

**For complete BREAD API documentation, see [BREAD_API_DOCUMENTATION.md](BREAD_API_DOCUMENTATION.md)**

### Authentication Endpoints

#### Register User

```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securePassword123",
  "confirm_password": "securePassword123"
}
```

**Success Response (201):**

```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (400/500):**

```json
{
  "error": "User with this email or username already exists",
  "details": [{"loc": ["email"], "msg": "..."}]
}
```

#### Login User

```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response (200):**

```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (401):**

```json
{
  "error": "Invalid email or password"
}
```

### Protected Endpoint

```http
GET /protected
Authorization: Bearer {access_token}
```

**Success Response (200):**

```json
{
  "message": "This is a protected route",
  "user_id": 1,
  "email": "user@example.com"
}
```

### Health Check

```http
GET /health
```

**Response (200):**

```json
{
  "status": "healthy"
}
```

## 🐳 Docker Hub Repository

Visit: `https://hub.docker.com/r/yourusername/jwt-auth-app`

**Available Tags:**
- `latest` - Most recent stable build
- `v1.0.0` - Specific version tags
- `develop` - Development branch builds

**Pull Image:**

```bash
docker pull yourusername/jwt-auth-app:latest
```

**Run Image:**

```bash
docker run -d \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/auth_db \
  -e JWT_SECRET_KEY=your-secret-key \
  yourusername/jwt-auth-app:latest
```

## 🔐 Security Considerations

1. **Password Security**: Passwords are hashed using PBKDF2 (werkzeug default)
2. **JWT Secret**: Never commit JWT secret to version control
3. **HTTPS**: Use HTTPS in production
4. **CORS**: Configure CORS for specific origins in production
5. **Rate Limiting**: Consider implementing rate limiting for production
6. **Environment Variables**: Use environment variables for sensitive data
7. **Token Expiry**: Tokens expire after 24 hours
8. **Input Validation**: All inputs validated with Pydantic

## 🆘 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 or 3000 already in use

**Solution:**
```bash
# Find process using port
lsof -i :5000  # On Mac/Linux
netstat -ano | findstr :5000  # On Windows

# Kill process or use different port
python app.py --port 5001
```

### Issue: Database connection error

**Solution:**
```bash
# Check database URL in .env
# For SQLite (development):
DATABASE_URL=sqlite:///users.db

# For PostgreSQL (production):
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
```

### Issue: Playwright tests fail

**Solution:**
```bash
# Install Playwright browsers
playwright install chromium

# Run tests with verbose output
pytest tests/test_auth.py -v -s
```

### Issue: Docker build fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t jwt-auth-app .
```

## 📝 Configuration

### Backend Configuration

Edit `backend/config.py` to modify:
- Database URL
- JWT expiration time
- Secret keys
- Debug mode

### Frontend Configuration

Edit `frontend/script.js` to modify:
- API URL
- Validation rules
- UI messages

### Docker Configuration

Edit `docker-compose.yml` to:
- Change ports
- Add environment variables
- Configure volumes
- Modify service versions

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of Module 13: JWT Authentication & CI/CD Pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy coding! 🚀**
