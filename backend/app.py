from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
import os
from dotenv import load_dotenv

from config import config
from models import Base, User
from schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from utils import generate_jwt_token, token_required, verify_jwt_token

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Enable CORS
CORS(app)

# Initialize database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

# ==================== Routes ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        data = request.get_json()
        
        # Validate request data
        register_schema = UserRegisterSchema(**data)
        
        session = Session()
        
        # Check if user already exists
        existing_user = session.query(User).filter(
            (User.email == register_schema.email) | (User.username == register_schema.username)
        ).first()
        
        if existing_user:
            session.close()
            return jsonify({
                'error': 'User with this email or username already exists'
            }), 400
        
        # Create new user
        new_user = User(
            email=register_schema.email,
            username=register_schema.username
        )
        new_user.set_password(register_schema.password)
        
        session.add(new_user)
        session.commit()
        
        # Generate JWT token
        token = generate_jwt_token(new_user.id, new_user.email)
        
        response = {
            'message': 'User registered successfully',
            'access_token': token,
            'token_type': 'Bearer',
            'user': new_user.to_dict()
        }
        
        session.close()
        return jsonify(response), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        data = request.get_json()
        
        # Validate request data
        login_schema = UserLoginSchema(**data)
        
        session = Session()
        
        # Find user by email
        user = session.query(User).filter(User.email == login_schema.email).first()
        
        if not user or not user.check_password(login_schema.password):
            session.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = generate_jwt_token(user.id, user.email)
        
        response = {
            'message': 'Login successful',
            'access_token': token,
            'token_type': 'Bearer',
            'user': user.to_dict()
        }
        
        session.close()
        return jsonify(response), 200
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/protected', methods=['GET'])
@token_required
def protected(payload):
    """Protected route that requires authentication."""
    return jsonify({
        'message': 'This is a protected route',
        'user_id': payload.get('user_id'),
        'email': payload.get('email')
    }), 200

@app.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint (client-side token removal)."""
    return jsonify({'message': 'Logout successful'}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
