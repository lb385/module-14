# BREAD Calculations API Documentation

This document describes the BREAD (Browse, Read, Edit, Add, Delete) endpoints for managing calculations in the JWT Authentication Application.

## Overview

The Calculations API allows authenticated users to create, retrieve, update, and delete mathematical calculations. All operations are user-specific, ensuring data isolation and security.

## Authentication

All endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

Tokens are obtained through the login or registration endpoints and remain valid for 24 hours.

## Base URL

- **Development**: `http://localhost:5050`
- **Production**: Based on deployment URL

## Endpoints

### 1. Browse Calculations (GET /calculations)

Retrieve all calculations belonging to the authenticated user.

**Request:**
```bash
curl -X GET http://localhost:5050/calculations \
  -H "Authorization: Bearer <token>"
```

**Response (200 OK):**
```json
{
  "message": "Calculations retrieved successfully",
  "calculations": [
    {
      "id": 1,
      "user_id": 1,
      "operation": "add",
      "operand1": 10.0,
      "operand2": 5.0,
      "result": 15.0,
      "created_at": "2024-04-28T10:30:00",
      "updated_at": "2024-04-28T10:30:00"
    },
    {
      "id": 2,
      "user_id": 1,
      "operation": "multiply",
      "operand1": 3.0,
      "operand2": 7.0,
      "result": 21.0,
      "created_at": "2024-04-28T11:15:00",
      "updated_at": "2024-04-28T11:15:00"
    }
  ]
}
```

**Error Responses:**
- 401 Unauthorized: Missing or invalid token
- 500 Internal Server Error: Database error

---

### 2. Read Single Calculation (GET /calculations/{id})

Retrieve details of a specific calculation.

**Request:**
```bash
curl -X GET http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer <token>"
```

**Response (200 OK):**
```json
{
  "message": "Calculation retrieved successfully",
  "calculation": {
    "id": 1,
    "user_id": 1,
    "operation": "add",
    "operand1": 10.0,
    "operand2": 5.0,
    "result": 15.0,
    "created_at": "2024-04-28T10:30:00",
    "updated_at": "2024-04-28T10:30:00"
  }
}
```

**Error Responses:**
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Calculation doesn't exist or unauthorized access
- 500 Internal Server Error: Database error

---

### 3. Add Calculation (POST /calculations)

Create a new calculation. The system automatically computes the result based on the operation and operands.

**Supported Operations:**
- `add` - Addition (operand1 + operand2)
- `subtract` - Subtraction (operand1 - operand2)
- `multiply` - Multiplication (operand1 × operand2)
- `divide` - Division (operand1 ÷ operand2)

**Request:**
```bash
curl -X POST http://localhost:5050/calculations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add",
    "operand1": 10,
    "operand2": 5
  }'
```

**Request Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| operation | string | Yes | One of: `add`, `subtract`, `multiply`, `divide` |
| operand1 | number | Yes | First operand (can be decimal) |
| operand2 | number | Yes | Second operand (cannot be 0 for division) |

**Response (201 Created):**
```json
{
  "message": "Calculation created successfully",
  "calculation": {
    "id": 3,
    "user_id": 1,
    "operation": "add",
    "operand1": 10.0,
    "operand2": 5.0,
    "result": 15.0,
    "created_at": "2024-04-28T12:00:00",
    "updated_at": "2024-04-28T12:00:00"
  }
}
```

**Error Responses:**
- 400 Bad Request: Invalid operation, missing fields, or division by zero
- 401 Unauthorized: Missing or invalid token
- 500 Internal Server Error: Database error

**Validation Errors (400):**
```json
{
  "error": "Validation error",
  "details": [
    {
      "loc": ["operation"],
      "msg": "Operation must be one of ['add', 'subtract', 'multiply', 'divide']",
      "type": "value_error"
    }
  ]
}
```

---

### 4. Edit Calculation (PATCH /calculations/{id})

Update a calculation. Only modified fields need to be included. The result is automatically recalculated.

**Request:**
```bash
curl -X PATCH http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "subtract",
    "operand1": 15
  }'
```

**Request Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| operation | string | No | New operation (partial update) |
| operand1 | number | No | New first operand |
| operand2 | number | No | New second operand |

**Response (200 OK):**
```json
{
  "message": "Calculation updated successfully",
  "calculation": {
    "id": 1,
    "user_id": 1,
    "operation": "subtract",
    "operand1": 15.0,
    "operand2": 5.0,
    "result": 10.0,
    "created_at": "2024-04-28T10:30:00",
    "updated_at": "2024-04-28T12:05:00"
  }
}
```

**Error Responses:**
- 400 Bad Request: Invalid data or division by zero
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Calculation doesn't exist or unauthorized access
- 500 Internal Server Error: Database error

**Alternative Method: PUT**
The update endpoint also supports PUT requests:
```bash
curl -X PUT http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

### 5. Delete Calculation (DELETE /calculations/{id})

Remove a calculation from the database.

**Request:**
```bash
curl -X DELETE http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer <token>"
```

**Response (200 OK):**
```json
{
  "message": "Calculation deleted successfully"
}
```

**Error Responses:**
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Calculation doesn't exist or unauthorized access
- 500 Internal Server Error: Database error

---

## Frontend Usage

### Creating a Calculation

```javascript
async function createCalculation(operation, operand1, operand2) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:5050/calculations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      operation,
      operand1: parseFloat(operand1),
      operand2: parseFloat(operand2)
    })
  });
  
  const data = await response.json();
  if (response.ok) {
    console.log('Calculation created:', data.calculation);
  } else {
    console.error('Error:', data.error);
  }
}
```

### Browsing Calculations

```javascript
async function getCalculations() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:5050/calculations', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  if (response.ok) {
    console.log('Calculations:', data.calculations);
  }
}
```

### Reading a Specific Calculation

```javascript
async function getCalculation(calculationId) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:5050/calculations/${calculationId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  if (response.ok) {
    console.log('Calculation:', data.calculation);
  }
}
```

### Updating a Calculation

```javascript
async function updateCalculation(calculationId, updates) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:5050/calculations/${calculationId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(updates)
  });
  
  const data = await response.json();
  if (response.ok) {
    console.log('Calculation updated:', data.calculation);
  }
}
```

### Deleting a Calculation

```javascript
async function deleteCalculation(calculationId) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`http://localhost:5050/calculations/${calculationId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('Calculation deleted:', data.message);
  }
}
```

## Data Types

### Calculation Object

```typescript
{
  id: number,                    // Unique identifier (auto-generated)
  user_id: number,              // ID of the user who owns this calculation
  operation: "add" | "subtract" | "multiply" | "divide",
  operand1: number,             // Can be integer or decimal
  operand2: number,             // Can be integer or decimal
  result: number,               // Calculated result
  created_at: string (ISO8601), // Timestamp when created
  updated_at: string (ISO8601)  // Timestamp when last updated
}
```

## Error Handling

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Or with validation details:

```json
{
  "error": "Validation error",
  "details": [
    {
      "loc": ["field_name"],
      "msg": "Error description",
      "type": "error_type"
    }
  ]
}
```

## Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input or business logic error |
| 401 | Unauthorized - Missing or invalid token |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server-side error |

## Rate Limiting

Currently, there are no rate limits implemented. This may be added in future versions.

## Security Considerations

1. **Token Expiration**: Tokens expire after 24 hours
2. **User Isolation**: Users can only access their own calculations
3. **Validation**: All inputs are validated server-side
4. **HTTPS**: Always use HTTPS in production
5. **Secrets**: Store JWT_SECRET_KEY securely in environment variables

## Examples

### Complete Workflow

```bash
# 1. Register a user
curl -X POST http://localhost:5050/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "password": "securePassword123",
    "confirm_password": "securePassword123"
  }'
# Response includes access_token

# 2. Create a calculation
TOKEN="<access_token_from_response>"
curl -X POST http://localhost:5050/calculations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "multiply",
    "operand1": 5,
    "operand2": 7
  }'

# 3. Browse all calculations
curl -X GET http://localhost:5050/calculations \
  -H "Authorization: Bearer $TOKEN"

# 4. Read a specific calculation
curl -X GET http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN"

# 5. Update the calculation
curl -X PATCH http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add",
    "operand1": 10
  }'

# 6. Delete the calculation
curl -X DELETE http://localhost:5050/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### "Invalid or expired token" Error

- Ensure token is included in Authorization header with "Bearer " prefix
- Check token hasn't expired (tokens valid for 24 hours)
- Re-login to get a new token

### "Calculation not found or unauthorized" Error

- Verify the calculation ID is correct
- Ensure you're accessing your own calculation (not another user's)
- Check that the calculation hasn't been deleted

### Division by Zero Error

- Do not use 0 as operand2 for division operations
- System will reject the request with a 400 error

### Validation Error on Creation

- Verify operation is one of: add, subtract, multiply, divide
- Ensure operands are valid numbers
- Check all required fields are provided
