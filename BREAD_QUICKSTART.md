# BREAD Operations Quick Start Guide

## Running the Application

### Step 1: Start the Backend

```bash
cd backend
python app.py
```

Backend runs on: `http://localhost:5050`

### Step 2: Start the Frontend (in a new terminal)

```bash
cd frontend
python -m http.server 3000
```

Frontend runs on: `http://localhost:3000`

## Testing the BREAD Operations

### 1. Register and Login

1. Navigate to `http://localhost:3000`
2. Click "Register" to create a new account
3. Fill in:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `password123`
   - Confirm Password: `password123`
4. Click "Register" - you'll be automatically logged in

### 2. Test Create (Add) Operation

1. In the "Create Calculation" section, fill in:
   - Operation: Select "Add"
   - First Operand: `10`
   - Second Operand: `5`
2. Click "Create Calculation"
3. Success message appears and calculation is added to the list

**Try other operations:**
- Subtract: `20` - `8` = `12`
- Multiply: `6` × `7` = `42`
- Divide: `20` ÷ `4` = `5`

### 3. Test Browse (Read List) Operation

1. After creating calculations, they appear in the "Your Calculations" section
2. Click "Refresh" to reload the list
3. Calculations display in a grid with:
   - Operation type (ADD, SUBTRACT, MULTIPLY, DIVIDE)
   - Operands displayed
   - Calculated result
   - Creation timestamp
   - Edit and Delete buttons

### 4. Test Read (View Details) Operation

1. Click the "Edit" button on any calculation
2. A modal opens showing:
   - Current calculation details
   - Current operation and operands
   - Current result
   - Edit form to make changes

### 5. Test Edit (Update) Operation

In the edit modal:

1. Try updating just the operation:
   - Select a different operation (e.g., change "Add" to "Subtract")
   - Click "Update Calculation"
   - Result recalculates

2. Try updating just operands:
   - Clear operation dropdown (no change)
   - Change First Operand: `15`
   - Click "Update Calculation"
   - Result recalculates with new operands

3. Try updating all fields:
   - Select new operation
   - Change both operands
   - Click "Update Calculation"
   - Everything updates and recalculates

### 6. Test Delete Operation

1. Click "Delete" button on any calculation
2. Confirm deletion in the dialog
3. Calculation is removed from the list
4. List refreshes automatically

## API Testing with cURL

### Get Access Token

```bash
curl -X POST http://localhost:5050/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curluser@example.com",
    "username": "curluser",
    "password": "testPassword123",
    "confirm_password": "testPassword123"
  }'
```

Copy the `access_token` from the response.

### Set Token Variable

```bash
TOKEN="your_access_token_here"
```

### Browse: GET All Calculations

```bash
curl -X GET http://localhost:5050/calculations \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "message": "Calculations retrieved successfully",
  "calculations": [
    {
      "id": 1,
      "user_id": 1,
      "operation": "add",
      "operand1": 10,
      "operand2": 5,
      "result": 15,
      ...
    }
  ]
}
```

### Add: POST New Calculation

```bash
curl -X POST http://localhost:5050/calculations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "multiply",
    "operand1": 5,
    "operand2": 7
  }'
```

**Expected Response:**
```json
{
  "message": "Calculation created successfully",
  "calculation": {
    "id": 2,
    "user_id": 1,
    "operation": "multiply",
    "operand1": 5,
    "operand2": 7,
    "result": 35,
    ...
  }
}
```

### Read: GET Specific Calculation

```bash
curl -X GET http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Edit: PATCH Update Calculation

```bash
curl -X PATCH http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "subtract",
    "operand1": 20
  }'
```

### Delete: DELETE Calculation

```bash
curl -X DELETE http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Only Calculation Tests

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

### Run Tests with Coverage Report

```bash
pip install pytest-cov
pytest tests/test_calculations.py --cov=backend --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Testing Different Scenarios

### Test Case 1: Create Multiple Operations

```
1. Create: 15 + 25 = 40
2. Create: 50 - 10 = 40
3. Create: 3 × 12 = 36
4. Create: 100 ÷ 5 = 20
5. Browse and verify all 4 in list
```

### Test Case 2: Update and Verify

```
1. Create: 10 + 5 = 15
2. Edit: Change to subtract → 10 - 5 = 5
3. Edit: Change operand1 to 20 → 20 - 5 = 15
4. Edit: Change operand2 to 3 → 20 - 3 = 17
5. Verify final result is 17
```

### Test Case 3: User Isolation

```
1. User A registers and creates: 10 + 20
2. User B registers
3. User B's calculation list shows only their calculations
4. User B cannot access User A's calculation via API
```

### Test Case 4: Error Handling

```
1. Try creating with no operation → Error
2. Try creating with invalid operation → Error
3. Try creating with non-numeric operand → Error
4. Try dividing by 0 → Error
5. Try accessing non-existent calculation → Error
6. Try accessing without token → Error
```

## Common Issues & Solutions

### Port Already in Use

**Port 3000 in use:**
```bash
cd frontend
python -m http.server 3001  # Use different port
```

**Port 5050 in use:**
Check what's running:
```bash
lsof -i :5050  # macOS/Linux
netstat -ano | findstr :5050  # Windows
```

### CORS Errors

- Ensure backend is running on `http://localhost:5050`
- Frontend script.js has correct API_URL
- CORS is enabled in Flask (CORS(app) in app.py)

### Token Expired

- Tokens valid for 24 hours
- Re-login to get a new token
- Or register again for a new account

### Database Errors

- Delete `users.db` and restart
- Check DATABASE_URL environment variable
- Ensure database directory is writable

## Next Steps

1. ✅ Test all BREAD operations in the UI
2. ✅ Test with cURL/Postman
3. ✅ Run the test suite
4. ✅ Review the API documentation
5. ✅ Deploy with Docker
6. ✅ Push to GitHub with CI/CD

## Documentation References

- **Full API Docs**: See [BREAD_API_DOCUMENTATION.md](BREAD_API_DOCUMENTATION.md)
- **Implementation Details**: See [BREAD_IMPLEMENTATION_SUMMARY.md](BREAD_IMPLEMENTATION_SUMMARY.md)
- **Verification Checklist**: See [IMPLEMENTATION_VERIFICATION.md](IMPLEMENTATION_VERIFICATION.md)
- **Main README**: See [README.md](README.md)

## Quick Command Reference

```bash
# Start backend
cd backend && python app.py

# Start frontend (new terminal)
cd frontend && python -m http.server 3000

# Run all tests
pytest tests/ -v

# Run calculation tests
pytest tests/test_calculations.py -v

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Support

For detailed information about specific operations, refer to:
- [BREAD_API_DOCUMENTATION.md](BREAD_API_DOCUMENTATION.md) - Complete API reference with examples
- [README.md](README.md) - General project documentation
- Code comments in `backend/app.py` - Endpoint implementations
- Code comments in `frontend/script.js` - Frontend functions

Happy testing! 🎉
