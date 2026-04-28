const API_URL = window.AUTH_APP_CONFIG?.apiUrl || 'http://localhost:5050';

// ==================== Utility Functions ====================

function clearErrors(formType) {
    const errorElements = document.querySelectorAll(`#${formType} .error`);
    errorElements.forEach(el => el.textContent = '');
}

function displayMessage(formType, message, type) {
    const messageEl = document.getElementById(`${formType}-message`);
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
}

function toggleForms(event) {
    event.preventDefault();
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginForm.style.display = loginForm.style.display === 'none' ? 'block' : 'none';
    registerForm.style.display = registerForm.style.display === 'none' ? 'block' : 'none';
    
    // Clear forms and messages
    document.getElementById('login').reset();
    document.getElementById('register').reset();
    clearErrors('login');
    clearErrors('register');
    document.getElementById('login-message').textContent = '';
    document.getElementById('register-message').textContent = '';
}

// ==================== Validation Functions ====================

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validatePassword(password) {
    return password && password.length >= 8;
}

function validateUsername(username) {
    return username && username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
}

// ==================== Client-side Validation ====================

document.getElementById('register-email').addEventListener('blur', function() {
    const email = this.value;
    const errorEl = document.getElementById('register-email-error');
    if (email && !validateEmail(email)) {
        errorEl.textContent = 'Please enter a valid email address';
    } else {
        errorEl.textContent = '';
    }
});

document.getElementById('register-username').addEventListener('blur', function() {
    const username = this.value;
    const errorEl = document.getElementById('register-username-error');
    if (username && !validateUsername(username)) {
        errorEl.textContent = 'Username must be at least 3 characters and contain only letters, numbers, and underscores';
    } else {
        errorEl.textContent = '';
    }
});

document.getElementById('register-password').addEventListener('blur', function() {
    const password = this.value;
    const errorEl = document.getElementById('register-password-error');
    if (password && !validatePassword(password)) {
        errorEl.textContent = 'Password must be at least 8 characters long';
    } else {
        errorEl.textContent = '';
    }
});

document.getElementById('register-confirm-password').addEventListener('blur', function() {
    const password = document.getElementById('register-password').value;
    const confirmPassword = this.value;
    const errorEl = document.getElementById('register-confirm-password-error');
    if (confirmPassword && password !== confirmPassword) {
        errorEl.textContent = 'Passwords do not match';
    } else {
        errorEl.textContent = '';
    }
});

document.getElementById('login-email').addEventListener('blur', function() {
    const email = this.value;
    const errorEl = document.getElementById('login-email-error');
    if (email && !validateEmail(email)) {
        errorEl.textContent = 'Please enter a valid email address';
    } else {
        errorEl.textContent = '';
    }
});

document.getElementById('login-password').addEventListener('blur', function() {
    const password = this.value;
    const errorEl = document.getElementById('login-password-error');
    if (password && !validatePassword(password)) {
        errorEl.textContent = 'Password must be at least 8 characters long';
    } else {
        errorEl.textContent = '';
    }
});

// ==================== Form Submission Handlers ====================

async function handleRegister(event) {
    event.preventDefault();
    clearErrors('register');
    
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    
    // Client-side validation
    let hasError = false;
    
    if (!validateEmail(email)) {
        document.getElementById('register-email-error').textContent = 'Please enter a valid email address';
        hasError = true;
    }
    
    if (!validateUsername(username)) {
        document.getElementById('register-username-error').textContent = 'Username must be at least 3 characters and contain only letters, numbers, and underscores';
        hasError = true;
    }
    
    if (!validatePassword(password)) {
        document.getElementById('register-password-error').textContent = 'Password must be at least 8 characters long';
        hasError = true;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('register-confirm-password-error').textContent = 'Passwords do not match';
        hasError = true;
    }
    
    if (hasError) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                username,
                password,
                confirm_password: confirmPassword
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayMessage('register', 'Registration successful! Logging you in...', 'success');
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            setTimeout(() => {
                showDashboard(data.user);
            }, 1500);
        } else {
            if (data.details) {
                // Handle Pydantic validation errors
                data.details.forEach(error => {
                    const field = error.loc[0];
                    const errorEl = document.getElementById(`register-${field}-error`);
                    if (errorEl) {
                        errorEl.textContent = error.msg;
                    }
                });
            } else {
                displayMessage('register', data.error || 'Registration failed', 'error');
            }
        }
    } catch (error) {
        displayMessage('register', 'An error occurred. Please try again.', 'error');
        console.error('Error:', error);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    clearErrors('login');
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    // Client-side validation
    let hasError = false;
    
    if (!validateEmail(email)) {
        document.getElementById('login-email-error').textContent = 'Please enter a valid email address';
        hasError = true;
    }
    
    if (!validatePassword(password)) {
        document.getElementById('login-password-error').textContent = 'Password must be at least 8 characters long';
        hasError = true;
    }
    
    if (hasError) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayMessage('login', 'Login successful! Redirecting...', 'success');
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            setTimeout(() => {
                showDashboard(data.user);
            }, 1500);
        } else {
            if (data.details) {
                // Handle Pydantic validation errors
                data.details.forEach(error => {
                    const field = error.loc[0];
                    const errorEl = document.getElementById(`login-${field}-error`);
                    if (errorEl) {
                        errorEl.textContent = error.msg;
                    }
                });
            } else {
                displayMessage('login', data.error || 'Login failed', 'error');
            }
        }
    } catch (error) {
        displayMessage('login', 'An error occurred. Please try again.', 'error');
        console.error('Error:', error);
    }
}

function showDashboard(user) {
    document.getElementById('auth-container').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
    
    const userInfoHtml = `
        <p><strong>Email:</strong> ${user.email}</p>
        <p><strong>Username:</strong> ${user.username}</p>
        <p><strong>User ID:</strong> ${user.id}</p>
    `;
    document.getElementById('user-info').innerHTML = userInfoHtml;
    
    // Load calculations when dashboard is shown
    refreshCalculations();
}

// ==================== Validation for Calculations ====================

function validateOperation(operation) {
    const allowedOperations = ['add', 'subtract', 'multiply', 'divide'];
    return allowedOperations.includes(operation);
}

function validateOperands(operand1, operand2) {
    return !isNaN(operand1) && !isNaN(operand2) && operand1 !== '' && operand2 !== '';
}

// ==================== Calculation BREAD Functions ====================

// Create (Add) - POST /calculations
async function handleCreateCalculation(event) {
    event.preventDefault();
    
    const operation = document.getElementById('operation').value;
    const operand1 = parseFloat(document.getElementById('operand1').value);
    const operand2 = parseFloat(document.getElementById('operand2').value);
    
    // Clear previous errors
    document.getElementById('operation-error').textContent = '';
    document.getElementById('operand1-error').textContent = '';
    document.getElementById('operand2-error').textContent = '';
    
    // Validation
    let hasError = false;
    
    if (!operation) {
        document.getElementById('operation-error').textContent = 'Please select an operation';
        hasError = true;
    }
    
    if (!validateOperands(operand1, operand2)) {
        if (isNaN(operand1) || operand1 === '') {
            document.getElementById('operand1-error').textContent = 'Please enter a valid number';
        }
        if (isNaN(operand2) || operand2 === '') {
            document.getElementById('operand2-error').textContent = 'Please enter a valid number';
        }
        hasError = true;
    }
    
    if (operation === 'divide' && operand2 === 0) {
        document.getElementById('operand2-error').textContent = 'Cannot divide by zero';
        hasError = true;
    }
    
    if (hasError) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_URL}/calculations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                operation,
                operand1,
                operand2
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayMessage('create-calc', 'Calculation created successfully!', 'success');
            document.getElementById('create-calc-form').reset();
            
            // Refresh calculations list
            setTimeout(() => {
                refreshCalculations();
            }, 1000);
        } else {
            if (data.details) {
                data.details.forEach(error => {
                    const field = error.loc[0];
                    const errorEl = document.getElementById(`${field}-error`);
                    if (errorEl) {
                        errorEl.textContent = error.msg;
                    }
                });
            } else {
                displayMessage('create-calc', data.error || 'Failed to create calculation', 'error');
            }
        }
    } catch (error) {
        displayMessage('create-calc', 'An error occurred. Please try again.', 'error');
        console.error('Error:', error);
    }
}

// Read & Browse - GET /calculations and GET /calculations/{id}
async function refreshCalculations() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_URL}/calculations`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        const calcList = document.getElementById('calculations-list');
        
        if (response.ok && data.calculations.length > 0) {
            let html = '<div class="calculations-grid">';
            data.calculations.forEach(calc => {
                html += `
                    <div class="calculation-card">
                        <h3>${calc.operation.toUpperCase()}</h3>
                        <p><strong>Operands:</strong> ${calc.operand1} ${calc.operation === 'add' ? '+' : calc.operation === 'subtract' ? '-' : calc.operation === 'multiply' ? '×' : '÷'} ${calc.operand2}</p>
                        <p><strong>Result:</strong> ${calc.result}</p>
                        <p class="created-at">Created: ${new Date(calc.created_at).toLocaleString()}</p>
                        <div class="card-actions">
                            <button onclick="openEditModal(${calc.id})" class="btn-small">Edit</button>
                            <button onclick="deleteCalculation(${calc.id})" class="btn-small btn-danger">Delete</button>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            calcList.innerHTML = html;
        } else if (response.ok) {
            calcList.innerHTML = '<p>No calculations yet. Create one to get started!</p>';
        } else {
            calcList.innerHTML = '<p>Failed to load calculations</p>';
        }
    } catch (error) {
        document.getElementById('calculations-list').innerHTML = '<p>Error loading calculations</p>';
        console.error('Error:', error);
    }
}

// Update (Edit) - PUT/PATCH /calculations/{id}
async function openEditModal(calculationId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_URL}/calculations/${calculationId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const calc = data.calculation;
            document.getElementById('edit-calc-form').dataset.calculationId = calculationId;
            document.getElementById('edit-operation').value = '';
            document.getElementById('edit-operand1').value = '';
            document.getElementById('edit-operand2').value = '';
            
            const resultHtml = `
                <h4>Current Calculation</h4>
                <p><strong>Operation:</strong> ${calc.operation.toUpperCase()}</p>
                <p><strong>Operand 1:</strong> ${calc.operand1}</p>
                <p><strong>Operand 2:</strong> ${calc.operand2}</p>
                <p><strong>Result:</strong> ${calc.result}</p>
            `;
            document.getElementById('edit-calc-result').innerHTML = resultHtml;
            
            document.getElementById('edit-calc-modal').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function closeEditModal() {
    document.getElementById('edit-calc-modal').style.display = 'none';
    document.getElementById('edit-calc-message').textContent = '';
}

async function handleUpdateCalculation(event) {
    event.preventDefault();
    
    const calculationId = document.getElementById('edit-calc-form').dataset.calculationId;
    const operation = document.getElementById('edit-operation').value || undefined;
    const operand1 = document.getElementById('edit-operand1').value ? parseFloat(document.getElementById('edit-operand1').value) : undefined;
    const operand2 = document.getElementById('edit-operand2').value ? parseFloat(document.getElementById('edit-operand2').value) : undefined;
    
    // Clear previous errors
    document.getElementById('edit-operation-error').textContent = '';
    document.getElementById('edit-operand1-error').textContent = '';
    document.getElementById('edit-operand2-error').textContent = '';
    
    // Build update object (only include fields that are not empty/undefined)
    const updateData = {};
    if (operation) updateData.operation = operation;
    if (operand1 !== undefined) updateData.operand1 = operand1;
    if (operand2 !== undefined) updateData.operand2 = operand2;
    
    if (Object.keys(updateData).length === 0) {
        displayMessage('edit-calc', 'Please fill in at least one field', 'error');
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_URL}/calculations/${calculationId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(updateData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayMessage('edit-calc', 'Calculation updated successfully!', 'success');
            
            setTimeout(() => {
                closeEditModal();
                refreshCalculations();
            }, 1000);
        } else {
            if (data.details) {
                data.details.forEach(error => {
                    const field = error.loc[0];
                    const errorEl = document.getElementById(`edit-${field}-error`);
                    if (errorEl) {
                        errorEl.textContent = error.msg;
                    }
                });
            } else {
                displayMessage('edit-calc', data.error || 'Failed to update calculation', 'error');
            }
        }
    } catch (error) {
        displayMessage('edit-calc', 'An error occurred. Please try again.', 'error');
        console.error('Error:', error);
    }
}

// Delete - DELETE /calculations/{id}
async function deleteCalculation(calculationId) {
    if (!confirm('Are you sure you want to delete this calculation?')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_URL}/calculations/${calculationId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            refreshCalculations();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to delete calculation');
        }
    } catch (error) {
        alert('An error occurred while deleting');
        console.error('Error:', error);
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    document.getElementById('auth-container').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
    
    document.getElementById('login').reset();
    document.getElementById('register').reset();
    clearErrors('login');
    clearErrors('register');
    document.getElementById('login-message').textContent = '';
    document.getElementById('register-message').textContent = '';
    
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
}

// ==================== Page Load ====================

window.addEventListener('load', function() {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        showDashboard(JSON.parse(user));
    }
});
