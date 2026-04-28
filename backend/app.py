from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
import os
from dotenv import load_dotenv

from config import config
from models import Base, User, Calculation
from schemas import (UserRegisterSchema, UserLoginSchema, TokenResponseSchema,
                     CalculationCreateSchema, CalculationUpdateSchema, CalculationResponseSchema)
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

# ==================== Helper Functions ====================

def perform_calculation(operation, operand1, operand2):
    """Perform a calculation based on operation type."""
    operations = {
        'add': lambda a, b: a + b,
        'subtract': lambda a, b: a - b,
        'multiply': lambda a, b: a * b,
        'divide': lambda a, b: a / b if b != 0 else None
    }
    
    if operation not in operations:
        return None
    
    return operations[operation](operand1, operand2)

# ==================== Calculation BREAD Endpoints ====================

@app.route('/calculations', methods=['GET'])
@token_required
def get_calculations(payload):
    """Browse: Retrieve all calculations for the logged-in user."""
    try:
        user_id = payload.get('user_id')
        session = Session()
        
        calculations = session.query(Calculation).filter(Calculation.user_id == user_id).all()
        session.close()
        
        return jsonify({
            'message': 'Calculations retrieved successfully',
            'calculations': [calc.to_dict() for calc in calculations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculations/<int:calculation_id>', methods=['GET'])
@token_required
def get_calculation(payload, calculation_id):
    """Read: Retrieve a specific calculation by ID."""
    try:
        user_id = payload.get('user_id')
        session = Session()
        
        calculation = session.query(Calculation).filter(
            (Calculation.id == calculation_id) & (Calculation.user_id == user_id)
        ).first()
        
        if not calculation:
            session.close()
            return jsonify({'error': 'Calculation not found or unauthorized'}), 404
        
        result = calculation.to_dict()
        session.close()
        
        return jsonify({
            'message': 'Calculation retrieved successfully',
            'calculation': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculations', methods=['POST'])
@token_required
def create_calculation(payload):
    """Add: Create a new calculation."""
    try:
        user_id = payload.get('user_id')
        data = request.get_json()
        
        # Validate request data
        calc_schema = CalculationCreateSchema(**data)
        
        # Perform calculation
        result = perform_calculation(calc_schema.operation, calc_schema.operand1, calc_schema.operand2)
        
        if result is None:
            return jsonify({'error': 'Invalid operation or division by zero'}), 400
        
        session = Session()
        
        # Create new calculation
        new_calculation = Calculation(
            user_id=user_id,
            operation=calc_schema.operation,
            operand1=calc_schema.operand1,
            operand2=calc_schema.operand2,
            result=result
        )
        
        session.add(new_calculation)
        session.commit()
        
        result_dict = new_calculation.to_dict()
        session.close()
        
        return jsonify({
            'message': 'Calculation created successfully',
            'calculation': result_dict
        }), 201
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculations/<int:calculation_id>', methods=['PUT', 'PATCH'])
@token_required
def update_calculation(payload, calculation_id):
    """Edit: Update a specific calculation."""
    try:
        user_id = payload.get('user_id')
        data = request.get_json()
        
        # Validate request data
        update_schema = CalculationUpdateSchema(**data)
        
        session = Session()
        
        calculation = session.query(Calculation).filter(
            (Calculation.id == calculation_id) & (Calculation.user_id == user_id)
        ).first()
        
        if not calculation:
            session.close()
            return jsonify({'error': 'Calculation not found or unauthorized'}), 404
        
        # Update fields if provided
        if update_schema.operation is not None:
            calculation.operation = update_schema.operation
        if update_schema.operand1 is not None:
            calculation.operand1 = update_schema.operand1
        if update_schema.operand2 is not None:
            calculation.operand2 = update_schema.operand2
        
        # Recalculate result
        result = perform_calculation(calculation.operation, calculation.operand1, calculation.operand2)
        if result is None:
            session.close()
            return jsonify({'error': 'Invalid operation or division by zero'}), 400
        
        calculation.result = result
        session.commit()
        
        result_dict = calculation.to_dict()
        session.close()
        
        return jsonify({
            'message': 'Calculation updated successfully',
            'calculation': result_dict
        }), 200
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculations/<int:calculation_id>', methods=['DELETE'])
@token_required
def delete_calculation(payload, calculation_id):
    """Delete: Remove a specific calculation."""
    try:
        user_id = payload.get('user_id')
        session = Session()
        
        calculation = session.query(Calculation).filter(
            (Calculation.id == calculation_id) & (Calculation.user_id == user_id)
        ).first()
        
        if not calculation:
            session.close()
            return jsonify({'error': 'Calculation not found or unauthorized'}), 404
        
        session.delete(calculation)
        session.commit()
        session.close()
        
        return jsonify({'message': 'Calculation deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, host='0.0.0.0', port=port)
