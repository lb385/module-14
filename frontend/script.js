const API_URL = window.AUTH_APP_CONFIG?.apiUrl || 'http://localhost:5000';

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
