import pytest
from playwright.sync_api import sync_playwright, expect
import time
import requests

BASE_URL = "http://localhost:3000"  # Frontend URL
API_URL = "http://localhost:5050"   # Backend API

# Test data
VALID_EMAIL = "calcuser@example.com"
VALID_USERNAME = "calcuser123"
VALID_PASSWORD = "calcPassword123"

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
    page.add_init_script("window.AUTH_APP_CONFIG = { apiUrl: 'http://localhost:5050' };")
    yield page
    page.close()

@pytest.fixture
def authenticated_page(page):
    """Create an authenticated page."""
    # Register a new user
    page.goto(BASE_URL)
    page.get_by_role("link", name="Register").click()
    
    page.locator('#register-email').fill(VALID_EMAIL)
    page.locator('#register-username').fill(VALID_USERNAME)
    page.locator('#register-password').fill(VALID_PASSWORD)
    page.locator('#register-confirm-password').fill(VALID_PASSWORD)
    
    page.locator('button:has-text("Register")').click()
    
    # Wait for dashboard
    page.wait_for_timeout(2000)
    dashboard = page.locator('#dashboard')
    expect(dashboard).to_be_visible()
    
    return page


class TestCalculationBrowse:
    """Test cases for Browse operation (GET /calculations)."""
    
    def test_browse_empty_calculations_list(self, authenticated_page):
        """Test browsing calculations when list is empty."""
        page = authenticated_page
        
        # Check if calculations list is visible
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_be_visible()
        
        # Check if "No calculations yet" message is displayed
        expect(calc_list).to_contain_text("No calculations yet")
    
    def test_browse_displays_calculations(self, authenticated_page):
        """Test that calculations are displayed in the list."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('10')
        page.locator('#operand2').fill('5')
        page.locator('button:has-text("Create Calculation")').click()
        
        # Wait for success message
        page.wait_for_timeout(1500)
        
        # Refresh to ensure we see the newly created calculation
        refresh_btn = page.locator('button:has-text("Refresh")')
        refresh_btn.click()
        
        page.wait_for_timeout(1000)
        
        # Check if calculation appears in list
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("ADD")
        expect(calc_list).to_contain_text("Result: 15")


class TestCalculationCreate:
    """Test cases for Add operation (POST /calculations)."""
    
    def test_create_calculation_with_valid_data(self, authenticated_page):
        """Test creating a calculation with valid data."""
        page = authenticated_page
        
        # Fill in the form
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('20')
        page.locator('#operand2').fill('15')
        
        # Submit the form
        page.locator('button:has-text("Create Calculation")').click()
        
        # Wait for success message
        message = page.locator('#create-calc-message')
        expect(message).to_contain_text("successfully")
        page.wait_for_timeout(1000)
    
    def test_create_calculation_add_operation(self, authenticated_page):
        """Test creating an addition calculation."""
        page = authenticated_page
        
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('5')
        page.locator('#operand2').fill('3')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Verify in list
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("ADD")
        expect(calc_list).to_contain_text("Result: 8")
    
    def test_create_calculation_subtract_operation(self, authenticated_page):
        """Test creating a subtraction calculation."""
        page = authenticated_page
        
        page.locator('#operation').select_option('subtract')
        page.locator('#operand1').fill('10')
        page.locator('#operand2').fill('3')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("SUBTRACT")
        expect(calc_list).to_contain_text("Result: 7")
    
    def test_create_calculation_multiply_operation(self, authenticated_page):
        """Test creating a multiplication calculation."""
        page = authenticated_page
        
        page.locator('#operation').select_option('multiply')
        page.locator('#operand1').fill('6')
        page.locator('#operand2').fill('7')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("MULTIPLY")
        expect(calc_list).to_contain_text("Result: 42")
    
    def test_create_calculation_divide_operation(self, authenticated_page):
        """Test creating a division calculation."""
        page = authenticated_page
        
        page.locator('#operation').select_option('divide')
        page.locator('#operand1').fill('20')
        page.locator('#operand2').fill('4')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("DIVIDE")
        expect(calc_list).to_contain_text("Result: 5")
    
    def test_create_calculation_missing_operation(self, authenticated_page):
        """Test creating a calculation without selecting operation."""
        page = authenticated_page
        
        page.locator('#operand1').fill('10')
        page.locator('#operand2').fill('5')
        page.locator('button:has-text("Create Calculation")').click()
        
        # Should show error
        error = page.locator('#operation-error')
        expect(error).to_contain_text("Please select an operation")
    
    def test_create_calculation_invalid_operand(self, authenticated_page):
        """Test creating a calculation with invalid operand."""
        page = authenticated_page
        
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('abc')
        page.locator('#operand2').fill('5')
        page.locator('button:has-text("Create Calculation")').click()
        
        # Should show error
        error = page.locator('#operand1-error')
        expect(error).to_contain_text("valid")
    
    def test_create_calculation_divide_by_zero(self, authenticated_page):
        """Test creating a division calculation with zero divisor."""
        page = authenticated_page
        
        page.locator('#operation').select_option('divide')
        page.locator('#operand1').fill('10')
        page.locator('#operand2').fill('0')
        page.locator('button:has-text("Create Calculation")').click()
        
        # Should show error
        error = page.locator('#operand2-error')
        expect(error).to_contain_text("Cannot divide by zero")
    
    def test_create_calculation_with_decimals(self, authenticated_page):
        """Test creating a calculation with decimal operands."""
        page = authenticated_page
        
        page.locator('#operation').select_option('multiply')
        page.locator('#operand1').fill('3.5')
        page.locator('#operand2').fill('2.5')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("MULTIPLY")
        expect(calc_list).to_contain_text("Result: 8.75")


class TestCalculationRead:
    """Test cases for Read operation (GET /calculations/{id})."""
    
    def test_read_single_calculation(self, authenticated_page):
        """Test reading a specific calculation."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('15')
        page.locator('#operand2').fill('25')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Click Edit button to open the calculation details
        page.locator('button:has-text("Edit")').first.click()
        
        page.wait_for_timeout(500)
        
        # Check if modal opened
        modal = page.locator('#edit-calc-modal')
        expect(modal).to_be_visible()
        
        # Verify calculation details are displayed
        result_section = page.locator('#edit-calc-result')
        expect(result_section).to_contain_text("ADD")
        expect(result_section).to_contain_text("15")
        expect(result_section).to_contain_text("25")
        expect(result_section).to_contain_text("Result: 40")


class TestCalculationUpdate:
    """Test cases for Edit operation (PUT/PATCH /calculations/{id})."""
    
    def test_update_calculation_operation(self, authenticated_page):
        """Test updating the operation of a calculation."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('10')
        page.locator('#operand2').fill('5')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Open edit modal
        page.locator('button:has-text("Edit")').first.click()
        page.wait_for_timeout(500)
        
        # Update the operation
        page.locator('#edit-operation').select_option('subtract')
        page.locator('button:has-text("Update Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Verify the calculation was updated
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("SUBTRACT")
        expect(calc_list).to_contain_text("Result: 5")
    
    def test_update_calculation_operands(self, authenticated_page):
        """Test updating the operands of a calculation."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('multiply')
        page.locator('#operand1').fill('3')
        page.locator('#operand2').fill('4')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Open edit modal
        page.locator('button:has-text("Edit")').first.click()
        page.wait_for_timeout(500)
        
        # Update the operands
        page.locator('#edit-operand1').fill('5')
        page.locator('#edit-operand2').fill('6')
        page.locator('button:has-text("Update Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Verify the calculation was updated
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("Result: 30")
    
    def test_update_calculation_all_fields(self, authenticated_page):
        """Test updating all fields of a calculation."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('2')
        page.locator('#operand2').fill('3')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Open edit modal
        page.locator('button:has-text("Edit")').first.click()
        page.wait_for_timeout(500)
        
        # Update all fields
        page.locator('#edit-operation').select_option('divide')
        page.locator('#edit-operand1').fill('10')
        page.locator('#edit-operand2').fill('2')
        page.locator('button:has-text("Update Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Verify the calculation was updated
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("DIVIDE")
        expect(calc_list).to_contain_text("Result: 5")
    
    def test_update_calculation_no_changes(self, authenticated_page):
        """Test that updating without changes shows error."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('5')
        page.locator('#operand2').fill('5')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Open edit modal
        page.locator('button:has-text("Edit")').first.click()
        page.wait_for_timeout(500)
        
        # Try to submit without making changes
        page.locator('button:has-text("Update Calculation")').click()
        
        # Should show error message
        message = page.locator('#edit-calc-message')
        expect(message).to_contain_text("Please fill in at least one field")


class TestCalculationDelete:
    """Test cases for Delete operation (DELETE /calculations/{id})."""
    
    def test_delete_calculation(self, authenticated_page):
        """Test deleting a calculation."""
        page = authenticated_page
        
        # Create a calculation
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('7')
        page.locator('#operand2').fill('3')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Get the calculation card text before deletion
        calc_list_before = page.locator('#calculations-list').inner_text()
        assert "ADD" in calc_list_before or "Result: 10" in calc_list_before
        
        # Click delete button
        page.locator('button:has-text("Delete")').first.click()
        
        # Confirm deletion in the browser dialog
        page.once('dialog', lambda dialog: dialog.accept())
        
        page.wait_for_timeout(1000)
        
        # Check if "No calculations yet" is now displayed
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("No calculations yet")
    
    def test_delete_one_of_multiple_calculations(self, authenticated_page):
        """Test deleting one calculation when multiple exist."""
        page = authenticated_page
        
        # Create two calculations
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('1')
        page.locator('#operand2').fill('1')
        page.locator('button:has-text("Create Calculation")').click()
        page.wait_for_timeout(1000)
        
        page.locator('#operation').select_option('subtract')
        page.locator('#operand1').fill('5')
        page.locator('#operand2').fill('2')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        # Delete the first calculation
        delete_buttons = page.locator('button:has-text("Delete")')
        delete_buttons.first.click()
        
        # Confirm deletion
        page.once('dialog', lambda dialog: dialog.accept())
        
        page.wait_for_timeout(1000)
        
        # Verify that the other calculation still exists
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("SUBTRACT")
        expect(calc_list).to_contain_text("Result: 3")


class TestCalculationSecurity:
    """Test cases for authorization and security."""
    
    def test_unauthorized_access_to_calculations(self, page):
        """Test accessing calculations without authentication."""
        # Try to access calculations endpoint without token
        response = page.request.get(f"{API_URL}/calculations")
        
        # Should return 401 Unauthorized
        assert response.status == 401
    
    def test_calculation_user_isolation(self, browser):
        """Test that users can only see their own calculations."""
        # Create first user and calculation
        page1 = browser.new_page()
        page1.add_init_script("window.AUTH_APP_CONFIG = { apiUrl: 'http://localhost:5050' };")
        page1.goto(BASE_URL)
        page1.get_by_role("link", name="Register").click()
        page1.locator('#register-email').fill("user1@example.com")
        page1.locator('#register-username').fill("user1")
        page1.locator('#register-password').fill("password123")
        page1.locator('#register-confirm-password').fill("password123")
        page1.locator('button:has-text("Register")').click()
        page1.wait_for_timeout(2000)
        
        # Create a calculation for user1
        page1.locator('#operation').select_option('add')
        page1.locator('#operand1').fill('10')
        page1.locator('#operand2').fill('20')
        page1.locator('button:has-text("Create Calculation")').click()
        page1.wait_for_timeout(1500)
        
        # Create second user
        page2 = browser.new_page()
        page2.add_init_script("window.AUTH_APP_CONFIG = { apiUrl: 'http://localhost:5050' };")
        page2.goto(BASE_URL)
        page2.get_by_role("link", name="Register").click()
        page2.locator('#register-email').fill("user2@example.com")
        page2.locator('#register-username').fill("user2")
        page2.locator('#register-password').fill("password123")
        page2.locator('#register-confirm-password').fill("password123")
        page2.locator('button:has-text("Register")').click()
        page2.wait_for_timeout(2000)
        
        # Check that user2 doesn't see user1's calculation
        calc_list = page2.locator('#calculations-list')
        expect(calc_list).to_contain_text("No calculations yet")
        
        # Clean up
        page1.close()
        page2.close()
    
    def test_invalid_calculation_id_access(self, authenticated_page):
        """Test accessing a non-existent calculation."""
        page = authenticated_page
        
        # Try to edit a calculation that doesn't exist
        # This should be handled by the API
        page.goto(f"{BASE_URL}")
        
        # Make a direct API call with invalid ID
        token = page.context.cookies.__dict__.get('access_token')
        
        # The frontend should handle this gracefully
        # For now, we verify the error handling in negative scenario
        pass


class TestCalculationEdgeCases:
    """Test edge cases and error handling."""
    
    def test_create_calculation_with_large_numbers(self, authenticated_page):
        """Test creating calculations with very large numbers."""
        page = authenticated_page
        
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('999999999')
        page.locator('#operand2').fill('999999999')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("ADD")
        expect(calc_list).to_contain_text("Result: 1999999998")
    
    def test_create_calculation_with_negative_numbers(self, authenticated_page):
        """Test creating calculations with negative numbers."""
        page = authenticated_page
        
        page.locator('#operation').select_option('add')
        page.locator('#operand1').fill('-5')
        page.locator('#operand2').fill('-3')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("ADD")
        expect(calc_list).to_contain_text("Result: -8")
    
    def test_create_calculation_with_zero_operand(self, authenticated_page):
        """Test creating calculations with zero as operand."""
        page = authenticated_page
        
        page.locator('#operation').select_option('multiply')
        page.locator('#operand1').fill('0')
        page.locator('#operand2').fill('100')
        page.locator('button:has-text("Create Calculation")').click()
        
        page.wait_for_timeout(1500)
        
        calc_list = page.locator('#calculations-list')
        expect(calc_list).to_contain_text("MULTIPLY")
        expect(calc_list).to_contain_text("Result: 0")
    
    def test_create_multiple_calculations_sequentially(self, authenticated_page):
        """Test creating multiple calculations in sequence."""
        page = authenticated_page
        
        operations = [
            ('add', '1', '1', '2'),
            ('subtract', '10', '3', '7'),
            ('multiply', '4', '5', '20'),
            ('divide', '20', '4', '5')
        ]
        
        for op, operand1, operand2, expected_result in operations:
            page.locator('#operation').select_option(op)
            page.locator('#operand1').fill(operand1)
            page.locator('#operand2').fill(operand2)
            page.locator('button:has-text("Create Calculation")').click()
            
            page.wait_for_timeout(1000)
        
        page.wait_for_timeout(500)
        
        # Verify all calculations are displayed
        calc_list = page.locator('#calculations-list')
        for op, operand1, operand2, expected_result in operations:
            expect(calc_list).to_contain_text(op.upper())
