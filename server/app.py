import uuid
from flask import Blueprint, Flask, jsonify, request, current_app
from flask_cors import CORS
from operator import itemgetter
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import pandas as pd
import jwt

HOTELS = [
    {
        'id': uuid.uuid4().hex,
        'name': 'Overlook Hotel',
        'address': '333 E Wonderview Ave, Estes Park, CO 80517',
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'The Grand Budapest Hotel',
        'address': 'The Republic of Zubrowka',
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'The Plaza Hotel',
        'address': '768 5th Ave, New York, NY 10019',
    }
]

BOOKINGS = [
    {
        'id': uuid.uuid4().hex,
        'from': datetime.datetime.strptime('02/03/2021','%d/%m/%Y').date(),
        'to': datetime.datetime.strptime('05/03/2021','%d/%m/%Y').date(),
        'name': 'Wes Anderson',
        'hotel': HOTELS[1].get("name"),
        'confirmed': False,
    },
    {
        'id': uuid.uuid4().hex,
        'from': datetime.datetime.strptime('25/02/2021','%d/%m/%Y').date(),
        'to': datetime.datetime.strptime('01/03/2021','%d/%m/%Y').date(),
        'name': 'Stanley Kubrick',
        'hotel': HOTELS[0].get("name"),
        'confirmed': True,
    }
]

USERS = [
    {
        'email': 'fedon@vue.com',
        'password': 'admin',
    }
]

# configuration
DEBUG = True
SECRET_KEY = 'mysupersecretkey'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

def remove_hotel(hotel_id):
    for hotel in HOTELS:
        if hotel['id'] == hotel_id:
            HOTELS.remove(hotel)
            return True
    return False

def remove_booking(booking_id):
    for booking in BOOKINGS:
        if booking['id'] == booking_id:
            BOOKINGS.remove(booking)
            return True
    return False

@app.route('/hotels', methods=['GET', 'POST'])
def all_hotels():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        HOTELS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'address': post_data.get('address')
        })
        response_object['message'] = 'Hotel added!'
    else:
        response_object['hotels'] = sorted(HOTELS, key=lambda k: k['name'])
    return jsonify(response_object)

@app.route('/bookings', methods=['GET', 'POST'])
def all_bookings():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        fromDate = datetime.datetime.strptime(post_data.get('from')[:10], '%Y-%m-%d').date().strftime('%d/%m/%Y')
        newFromformat = datetime.datetime.strptime(str(fromDate),'%d/%m/%Y').date()
        toDate = datetime.datetime.strptime(post_data.get('to')[:10], '%Y-%m-%d').date().strftime('%d/%m/%Y')
        newToformat = datetime.datetime.strptime(str(toDate),'%d/%m/%Y').date()
        BOOKINGS.append({
            'id': uuid.uuid4().hex,
            'from': newFromformat,
            'to': newToformat,
            'name': post_data.get('name'),
            'hotel': post_data.get('hotel'),
            'confirmed': post_data.get('confirmed')
        })
        response_object['message'] = 'Booking added!'
    else:
        response_object['bookings'] = sorted(BOOKINGS, key=lambda k: k['from'], reverse=True)
    return jsonify(response_object)

@app.route('/hotels/<hotel_id>', methods=['PUT', 'DELETE'])
def single_hotel(hotel_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_hotel(hotel_id)
        HOTELS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'address': post_data.get('address')
        })
        response_object['message'] = 'Hotel updated!'
    if request.method == 'DELETE':
        remove_hotel(hotel_id)
        response_object['message'] = 'Hotel removed!'
    return jsonify(response_object)

@app.route('/bookings/<booking_id>', methods=['PUT', 'DELETE'])
def single_booking(booking_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_booking(booking_id)
        fromDate = datetime.datetime.strptime(post_data.get('from')[:10], '%Y-%m-%d').date().strftime('%d/%m/%Y')
        newFromformat = datetime.datetime.strptime(str(fromDate),'%d/%m/%Y').date()
        toDate = datetime.datetime.strptime(post_data.get('to')[:10], '%Y-%m-%d').date().strftime('%d/%m/%Y')
        newToformat = datetime.datetime.strptime(str(toDate),'%d/%m/%Y').date()
        BOOKINGS.append({
            'id': uuid.uuid4().hex,
            'from': newFromformat,
            'to': newToformat,
            'name': post_data.get('name'),
            'hotel': post_data.get('hotel'),
            'confirmed': post_data.get('confirmed')
        })
        response_object['message'] = 'Booking updated!'
    if request.method == 'DELETE':
        remove_booking(booking_id)
        response_object['message'] = 'Booking removed!'
    return jsonify(response_object)

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user['email'],
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({ 'token': token })

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

def authenticate(**kwargs):
    email = kwargs.get('email')
    password = kwargs.get('password')
    if not email or not password:
        return None

    for user in USERS:
        if user['email'] == email:
            userpassword = generate_password_hash(user['password'], method='sha256')
            if user['password'] == password:
                return user

    return None

if __name__ == '__main__':
    app.run()
