# Testing Guide

## Comprehensive E2E Testing Documentation

This guide provides detailed instructions for running and understanding the Playwright E2E tests.

---

## 📋 Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

---

## 🧪 Test Execution

### Run All Tests

```bash
pytest tests/test_auth.py -v
```

**Expected Output:**
```
tests/test_auth.py::TestRegistration::test_register_page_loads PASSED
tests/test_auth.py::TestRegistration::test_register_with_valid_data PASSED
tests/test_auth.py::TestRegistration::test_register_with_short_password PASSED
...
======================== 15 passed in 23.45s ========================
```

### Run Specific Test Class

```bash
# Registration tests only
pytest tests/test_auth.py::TestRegistration -v

# Login tests only
pytest tests/test_auth.py::TestLogin -v

# Token tests only
pytest tests/test_auth.py::TestTokenHandling -v
```

### Run Specific Test

```bash
pytest tests/test_auth.py::TestRegistration::test_register_with_valid_data -v
```

### Run with Output Capture Disabled

```bash
pytest tests/test_auth.py -v -s
```

This shows print statements during test execution.

### Run with Detailed Failure Info

```bash
pytest tests/test_auth.py -vv --tb=long
```

### Run Tests in Parallel (faster)

```bash
pip install pytest-xdist
pytest tests/test_auth.py -n auto -v
```

---

## 🔍 Test Descriptions

### Registration Tests (TestRegistration)

#### 1. test_register_page_loads
**Purpose**: Verify registration page loads and form elements are visible

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Verify email, username, password, and confirm password inputs are visible

**Expected Result**: ✅ All form fields should be visible

**Why This Matters**: Ensures the form is properly loaded before user interaction

---

#### 2. test_register_with_valid_data
**Purpose**: Test complete registration flow with valid data

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Fill in valid registration data:
  - Email: testuser@example.com
  - Username: testuser123
  - Password: securePassword123
  - Confirm: securePassword123
- Submit form
- Verify success message appears
- Verify dashboard is shown (user logged in)

**Expected Result**: ✅ User should be registered and logged in successfully

**API Calls:**
- POST /register with user data
- Returns 201 Created with JWT token
- User stored in database

**Why This Matters**: Validates the happy path of registration

---

#### 3. test_register_with_short_password
**Purpose**: Test validation when password is too short

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Attempt to enter password with 5 characters
- Trigger blur event on password field
- Check for error message

**Expected Result**: ❌ Error message should show "at least 8 characters"

**Client-Side Validation**: Catches error before server call

**Why This Matters**: Prevents invalid data from being sent to server

---

#### 4. test_register_with_mismatched_passwords
**Purpose**: Test validation when password confirmation doesn't match

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Enter password: Password123
- Enter confirm password: DifferentPassword123
- Trigger blur event
- Check for error message

**Expected Result**: ❌ Error message should show "not match"

**Why This Matters**: Prevents user typos in password

---

#### 5. test_register_with_invalid_email
**Purpose**: Test validation when email format is invalid

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Enter invalid email: "invalid-email" (no @)
- Trigger blur event on email field
- Check for error message

**Expected Result**: ❌ Error message should show "valid email"

**Why This Matters**: Ensures proper email format

---

#### 6. test_register_with_short_username
**Purpose**: Test HTML5 validation when username is too short

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Enter username with only 2 characters: "ab"
- Check HTML5 validity

**Expected Result**: ❌ HTML5 validation should fail

**Why This Matters**: Username must be at least 3 characters

---

### Login Tests (TestLogin)

#### 1. test_login_page_loads
**Purpose**: Verify login page loads and form elements are visible

**Expected Result**: ✅ Email and password inputs should be visible

---

#### 2. test_login_with_correct_credentials
**Purpose**: Test complete login flow with correct credentials

**Actions:**
1. Register a new user (with unique email/username)
2. Verify dashboard appears
3. Click logout
4. Go back to login form
5. Enter registered credentials
6. Submit form
7. Verify success message and dashboard

**Expected Result**: ✅ User should be logged in successfully

**API Calls:**
- POST /register (creates user)
- POST /login (authenticates user)
- Returns JWT token

**Why This Matters**: Validates login functionality after registration

---

#### 3. test_login_with_wrong_password
**Purpose**: Test login rejection with incorrect password

**Actions:**
- Navigate to login page
- Enter valid email but wrong password
- Submit form
- Check for error message

**Expected Result**: ❌ Error message should show "Invalid"

**HTTP Status**: 401 Unauthorized

**Why This Matters**: Ensures wrong credentials are rejected

---

#### 4. test_login_with_invalid_email
**Purpose**: Test validation when email format is invalid

**Actions:**
- Navigate to login page
- Enter invalid email format
- Trigger blur event
- Check for error message

**Expected Result**: ❌ Error message should show "valid email"

---

#### 5. test_login_with_short_password
**Purpose**: Test validation when password is too short

**Actions:**
- Navigate to login page
- Enter short password (< 8 chars)
- Trigger blur event
- Check for error message

**Expected Result**: ❌ Error message should show "at least 8 characters"

---

### Form Toggling Tests (TestFormToggling)

#### 1. test_toggle_to_register_form
**Purpose**: Verify user can switch from login to register

**Actions:**
- Navigate to http://localhost:3000
- Verify login form is visible
- Click "Register" link
- Verify register form is visible

**Expected Result**: ✅ Forms should toggle correctly

---

#### 2. test_toggle_to_login_form
**Purpose**: Verify user can switch from register to login

**Actions:**
- Navigate to http://localhost:3000
- Click "Register" link
- Verify register form is visible
- Click "Login" link
- Verify login form is visible

**Expected Result**: ✅ Forms should toggle correctly

---

### Token Handling Tests (TestTokenHandling)

#### 1. test_token_stored_in_localstorage_after_login
**Purpose**: Verify JWT token is properly stored after registration

**Actions:**
1. Register new user
2. Wait for dashboard
3. Query localStorage for access_token
4. Verify token exists and has content

**Expected Result**: ✅ localStorage should contain access_token

**Token Format**: JWT (three parts separated by dots)

**Why This Matters**: Token must be stored for authenticated requests

---

#### 2. test_token_cleared_after_logout
**Purpose**: Verify JWT token is cleared from localStorage after logout

**Actions:**
1. Register and login user
2. Verify token in localStorage
3. Click logout
4. Query localStorage again
5. Verify token is null

**Expected Result**: ✅ localStorage should not contain access_token

**Why This Matters**: Prevents unauthorized access after logout

---

## 🛠️ Debugging Tests

### Enable Headed Mode (See Browser)

```bash
# This won't work with default Playwright setup, but shows the test
# Modify conftest.py to use:
browser = playwright.chromium.launch(headless=False)
```

### Add Debug Breakpoints

```python
# In test file
page.pause()  # Pauses execution, opens inspector
```

### Capture Screenshots

```python
# In test file
page.screenshot(path='screenshot.png')
```

### Capture Video

```python
# In test file, modify fixture:
page = browser.new_page(record_video_dir='videos/')
```

### Print Debug Info

```bash
# Run with output capture disabled
pytest tests/test_auth.py -s -v
```

---

## 📊 Test Metrics

### Execution Time

```bash
# Run with timing information
pytest tests/test_auth.py -v --durations=10
```

**Expected Times:**
- Single test: 1-3 seconds
- All 15 tests: 20-30 seconds
- Full CI/CD run: 3-5 minutes

### Coverage Report

```bash
pip install pytest-cov
pytest tests/test_auth.py --cov=backend --cov-report=html
# Opens htmlcov/index.html
```

---

## 🔧 Common Test Issues & Solutions

### Issue: Tests Fail with "Connection Refused"

**Cause**: Backend or frontend not running

**Solution:**
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
cd frontend
python -m http.server 3000

# Terminal 3: Run tests
pytest tests/test_auth.py -v
```

---

### Issue: "Timeout waiting for selector"

**Cause**: Element not found or takes too long to appear

**Debug:**
```python
# Check that selectors are correct
page.locator('#login-email')
page.locator('button:has-text("Login")')
```

---

### Issue: Database State Between Tests

**Cause**: User already exists from previous test

**Current Solution**: Use unique email per test
```python
test_email = f"test_{int(time.time())}@example.com"
```

---

### Issue: Tests Pass Locally but Fail in CI/CD

**Likely Cause**: Service timing issues

**Solution in Workflow:**
```yaml
- name: Start services
  run: sleep 3  # Wait for services to be ready
```

---

## 📈 Performance Optimization

### Parallel Test Execution

```bash
pip install pytest-xdist
pytest tests/test_auth.py -n auto -v
```

**Note**: Parallel may cause issues if tests use shared database state

### Skip Slow Tests During Development

```bash
# Add marker to test
@pytest.mark.skip(reason="Slow test")
def test_something():
    pass

# Run without skipped tests
pytest tests/test_auth.py -v -m "not skip"
```

---

## 🚀 CI/CD Integration

### GitHub Actions Runs Tests

The workflow in `.github/workflows/ci-cd.yml`:
1. Sets up Python 3.11
2. Installs dependencies
3. Starts PostgreSQL
4. Starts backend and frontend
5. Runs E2E tests
6. Uploads results as artifact
7. Builds Docker image if tests pass

### View Test Results in GitHub

1. Go to repository
2. Click "Actions" tab
3. Click workflow run
4. Click "Run Playwright E2E tests" step
5. See test output
6. Download artifacts (playwright-report)

---

## 📚 Test Best Practices

### ✅ Do's

- ✅ Use descriptive test names
- ✅ Test one thing per test
- ✅ Use unique test data
- ✅ Clean up state after tests
- ✅ Use explicit waits for async operations
- ✅ Document complex test logic
- ✅ Group related tests in classes

### ❌ Don'ts

- ❌ Don't depend on test execution order
- ❌ Don't share state between tests
- ❌ Don't use implicit waits
- ❌ Don't test implementation details
- ❌ Don't have tests that are too long
- ❌ Don't ignore test failures

---

## 🎯 Test Scenarios Coverage

| Scenario | Test | Status |
|----------|------|--------|
| Valid registration | test_register_with_valid_data | ✅ |
| Duplicate email | Covered by 400 error | ✅ |
| Short password | test_register_with_short_password | ✅ |
| Invalid email | test_register_with_invalid_email | ✅ |
| Valid login | test_login_with_correct_credentials | ✅ |
| Wrong password | test_login_with_wrong_password | ✅ |
| Token storage | test_token_stored_in_localstorage | ✅ |
| Token cleanup | test_token_cleared_after_logout | ✅ |

---

## 📝 Writing Custom Tests

### Test Template

```python
def test_new_feature(page):
    """Test description explaining what is being tested."""
    # Arrange: Navigate and set up
    page.goto(BASE_URL)
    
    # Act: Perform actions
    page.locator('#email').fill('test@example.com')
    page.locator('button').click()
    
    # Assert: Verify results
    success_message = page.locator('#message')
    expect(success_message).to_contain_text("success")
```

### Using Selectors

```python
# ID selector
page.locator('#login-email')

# Text selector
page.locator('button:has-text("Login")')

# Class selector
page.locator('.form-container')

# Attribute selector
page.locator('input[type="email"]')

# Combined
page.locator('#register-form input[type="password"]')
```

### Assertions

```python
# Visibility
assert element.is_visible()

# Text content
expect(element).to_contain_text("expected text")

# Class
expect(element).to_have_class("success")

# Attribute
expect(input_element).to_have_value("expected value")

# Count
expect(page.locator('.item')).to_have_count(5)
```

---

## 🔄 Continuous Testing

### Watch Mode (During Development)

```bash
# Install pytest-watch
pip install pytest-watch

# Watch for file changes
ptw tests/test_auth.py
```

---

## 📞 Support & Troubleshooting

For detailed troubleshooting, see main README.md "Troubleshooting" section.

For test-specific issues, check:
- Test output for error messages
- Browser DevTools (if using headed mode)
- Server logs (backend/frontend terminals)
- Database state (sqlite3 backend/users.db)

---

**Last Updated**: April 21, 2026  
**Version**: 1.0  
**Status**: ✅ Complete

