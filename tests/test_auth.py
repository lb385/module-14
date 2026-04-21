import pytest
from playwright.sync_api import sync_playwright, expect
import time

BASE_URL = "http://localhost:3000"  # Frontend URL (serve with simple server)
API_URL = "http://localhost:5000"   # Backend API

# Test data
VALID_EMAIL = "testuser@example.com"
VALID_USERNAME = "testuser123"
VALID_PASSWORD = "securePassword123"
INVALID_EMAIL = "invalid-email"
SHORT_PASSWORD = "short"
WRONG_PASSWORD = "wrongPassword123"

@pytest.fixture(scope="session")
def browser():
    """Browser fixture for all tests."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    """Page fixture for each test."""
    page = browser.new_page()
    yield page
    page.close()

class TestRegistration:
    """Test cases for user registration."""
    
    def test_register_page_loads(self, page):
        """Test that the registration page loads successfully."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Check if registration form is visible
        email_input = page.locator('#register-email')
        assert email_input.is_visible()
        
        username_input = page.locator('#register-username')
        assert username_input.is_visible()
        
        password_input = page.locator('#register-password')
        assert password_input.is_visible()
    
    def test_register_with_valid_data(self, page):
        """Test successful registration with valid data."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Fill in the form
        page.locator('#register-email').fill(VALID_EMAIL)
        page.locator('#register-username').fill(VALID_USERNAME)
        page.locator('#register-password').fill(VALID_PASSWORD)
        page.locator('#register-confirm-password').fill(VALID_PASSWORD)
        
        # Submit the form
        page.locator('button:has-text("Register")').click()
        
        # Wait for success message
        success_message = page.locator('#register-message')
        expect(success_message).to_contain_text("successful")
        expect(success_message).to_have_class("success")
        
        # Check if dashboard is shown (user is logged in)
        page.wait_for_timeout(2000)
        dashboard = page.locator('#dashboard')
        assert dashboard.is_visible()
    
    def test_register_with_short_password(self, page):
        """Test registration with a password that's too short."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Fill in the form with short password
        page.locator('#register-email').fill(VALID_EMAIL)
        page.locator('#register-username').fill(VALID_USERNAME)
        page.locator('#register-password').fill(SHORT_PASSWORD)
        page.locator('#register-confirm-password').fill(SHORT_PASSWORD)
        
        # Check client-side error appears
        page.locator('#register-password').blur()
        error_message = page.locator('#register-password-error')
        expect(error_message).to_contain_text("at least 8 characters")
    
    def test_register_with_mismatched_passwords(self, page):
        """Test registration with mismatched passwords."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Fill in the form with mismatched passwords
        page.locator('#register-email').fill(VALID_EMAIL)
        page.locator('#register-username').fill(VALID_USERNAME)
        page.locator('#register-password').fill(VALID_PASSWORD)
        page.locator('#register-confirm-password').fill("differentPassword123")
        
        # Check client-side error appears
        page.locator('#register-confirm-password').blur()
        error_message = page.locator('#register-confirm-password-error')
        expect(error_message).to_contain_text("not match")
    
    def test_register_with_invalid_email(self, page):
        """Test registration with invalid email format."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Fill in the form with invalid email
        page.locator('#register-email').fill(INVALID_EMAIL)
        
        # Check client-side error appears
        page.locator('#register-email').blur()
        error_message = page.locator('#register-email-error')
        expect(error_message).to_contain_text("valid email")
    
    def test_register_with_short_username(self, page):
        """Test registration with username that's too short."""
        page.goto(BASE_URL)
        # Switch to registration form
        page.locator("text=Register").click()
        
        # Fill in the form with short username
        page.locator('#register-email').fill(VALID_EMAIL)
        page.locator('#register-username').fill("ab")
        page.locator('#register-password').fill(VALID_PASSWORD)
        page.locator('#register-confirm-password').fill(VALID_PASSWORD)
        
        # Check HTML5 validation
        username_input = page.locator('#register-username')
        is_valid = username_input.evaluate('el => el.checkValidity()')
        assert not is_valid

class TestLogin:
    """Test cases for user login."""
    
    def test_login_page_loads(self, page):
        """Test that the login page loads successfully."""
        page.goto(BASE_URL)
        
        # Check if login form is visible
        email_input = page.locator('#login-email')
        assert email_input.is_visible()
        
        password_input = page.locator('#login-password')
        assert password_input.is_visible()
    
    def test_login_with_correct_credentials(self, page):
        """Test successful login with correct credentials."""
        # First, register a user
        page.goto(BASE_URL)
        page.locator("text=Register").click()
        
        test_email = f"login_test_{int(time.time())}@example.com"
        test_username = f"user_{int(time.time())}"
        test_password = "testPassword123"
        
        page.locator('#register-email').fill(test_email)
        page.locator('#register-username').fill(test_username)
        page.locator('#register-password').fill(test_password)
        page.locator('#register-confirm-password').fill(test_password)
        page.locator('button:has-text("Register")').click()
        
        # Wait for dashboard to appear
        page.wait_for_timeout(2000)
        dashboard = page.locator('#dashboard')
        assert dashboard.is_visible()
        
        # Logout
        page.locator('button:has-text("Logout")').click()
        
        # Now test login
        page.wait_for_timeout(1000)
        login_form = page.locator('#login-form')
        assert login_form.is_visible()
        
        # Fill in login form
        page.locator('#login-email').fill(test_email)
        page.locator('#login-password').fill(test_password)
        page.locator('button:has-text("Login")').click()
        
        # Check for success and dashboard
        success_message = page.locator('#login-message')
        expect(success_message).to_contain_text("successful")
        
        page.wait_for_timeout(2000)
        dashboard = page.locator('#dashboard')
        assert dashboard.is_visible()
    
    def test_login_with_wrong_password(self, page):
        """Test login with wrong password."""
        page.goto(BASE_URL)
        
        # Fill in login form with wrong password
        page.locator('#login-email').fill(VALID_EMAIL)
        page.locator('#login-password').fill(WRONG_PASSWORD)
        page.locator('button:has-text("Login")').click()
        
        # Check for error message
        error_message = page.locator('#login-message')
        page.wait_for_timeout(1000)
        expect(error_message).to_contain_text("Invalid")
        expect(error_message).to_have_class("error")
    
    def test_login_with_invalid_email(self, page):
        """Test login with invalid email format."""
        page.goto(BASE_URL)
        
        # Fill in login form with invalid email
        page.locator('#login-email').fill(INVALID_EMAIL)
        
        # Check client-side error appears
        page.locator('#login-email').blur()
        error_message = page.locator('#login-email-error')
        expect(error_message).to_contain_text("valid email")
    
    def test_login_with_short_password(self, page):
        """Test login with short password."""
        page.goto(BASE_URL)
        
        # Fill in login form with short password
        page.locator('#login-email').fill(VALID_EMAIL)
        page.locator('#login-password').fill(SHORT_PASSWORD)
        
        # Check client-side error appears
        page.locator('#login-password').blur()
        error_message = page.locator('#login-password-error')
        expect(error_message).to_contain_text("at least 8 characters")

class TestFormToggling:
    """Test cases for form toggling between login and register."""
    
    def test_toggle_to_register_form(self, page):
        """Test toggling from login to register form."""
        page.goto(BASE_URL)
        
        # Start on login form
        login_form = page.locator('#login-form')
        assert login_form.is_visible()
        
        # Click on register link
        page.locator("text=Register").click()
        
        # Check register form is now visible
        register_form = page.locator('#register-form')
        assert register_form.is_visible()
    
    def test_toggle_to_login_form(self, page):
        """Test toggling from register to login form."""
        page.goto(BASE_URL)
        
        # Switch to register form
        page.locator("text=Register").click()
        register_form = page.locator('#register-form')
        assert register_form.is_visible()
        
        # Click on login link
        page.locator("text=Login").click()
        
        # Check login form is now visible
        login_form = page.locator('#login-form')
        assert login_form.is_visible()

class TestTokenHandling:
    """Test cases for JWT token handling."""
    
    def test_token_stored_in_localstorage_after_login(self, page):
        """Test that JWT token is stored in localStorage after login."""
        page.goto(BASE_URL)
        
        # Register a new user
        page.locator("text=Register").click()
        
        test_email = f"token_test_{int(time.time())}@example.com"
        test_username = f"user_{int(time.time())}"
        test_password = "tokenPassword123"
        
        page.locator('#register-email').fill(test_email)
        page.locator('#register-username').fill(test_username)
        page.locator('#register-password').fill(test_password)
        page.locator('#register-confirm-password').fill(test_password)
        page.locator('button:has-text("Register")').click()
        
        page.wait_for_timeout(2000)
        
        # Check that token is in localStorage
        token = page.evaluate('() => localStorage.getItem("access_token")')
        assert token is not None
        assert len(token) > 0
    
    def test_token_cleared_after_logout(self, page):
        """Test that JWT token is cleared from localStorage after logout."""
        page.goto(BASE_URL)
        
        # Register and login
        page.locator("text=Register").click()
        
        test_email = f"logout_test_{int(time.time())}@example.com"
        test_username = f"user_{int(time.time())}"
        test_password = "logoutPassword123"
        
        page.locator('#register-email').fill(test_email)
        page.locator('#register-username').fill(test_username)
        page.locator('#register-password').fill(test_password)
        page.locator('#register-confirm-password').fill(test_password)
        page.locator('button:has-text("Register")').click()
        
        page.wait_for_timeout(2000)
        
        # Click logout
        page.locator('button:has-text("Logout")').click()
        page.wait_for_timeout(1000)
        
        # Check that token is cleared
        token = page.evaluate('() => localStorage.getItem("access_token")')
        assert token is None
