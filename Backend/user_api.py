from flask import Blueprint, request, jsonify, session
# Assume User and Trip models are defined elsewhere and imported here
# from models import User, Trip

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Replace with actual user lookup and password check
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in'})
    return jsonify({'error': 'Invalid credentials'}), 401

@user_api.route('/api/user/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    user = User.query.get(user_id)
    return jsonify({'name': user.name, 'email': user.email})

@user_api.route('/api/user/trips', methods=['GET'])
def user_trips():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([trip.to_dict() for trip in trips]) 