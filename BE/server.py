from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId
from dotenv import load_dotenv
import os
from flask_cors import CORS, cross_origin
from mongo_DB_client import MongoDBClient
from datetime import datetime

app = Flask(__name__)
# CORS(app, origins=['http://localhost:4200', '*'])
CORS(app, support_credentials=True)
print('Server started')

# Load environment variables from .env file
load_dotenv()

def connectDB():
    try:
        username = quote_plus(os.getenv('MONGO_USERNAME'))
        password = quote_plus(os.getenv('MONGO_PASSWORD'))
        # uri = 'mongodb+srv://%s:%s@c1.2ogkv.mongodb.net/?retryWrites=true&w=majority&appName=C1' % (username, password)
        # db = client['Deepthi'] 

        uri = 'mongodb://localhost:27017'

        database_name = 'Deepthi'
        db = MongoDBClient(uri, database_name)

        print('Connected to MongoDB')
        return db
    except Exception as e:
        print('Error connecting to MongoDB')
        print(e)
        return None


db = connectDB()

if db is None:
    print('Error connecting to MongoDB')
    exit(1)


# print(Appointments)

@app.post('/appointment')
@cross_origin(supports_credentials=True)
def create_appointment():
    Appointments = db.database.appointments

    data = request.json
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    phone = data.get('phone')
    message = data.get('message')

    if not name or not email or not date or not phone:
        return jsonify({'error': 'Please fill all fields'}), 400

    new_appointment = {
        'name': name,
        'email': email,
        'date': date,
        'phone': phone,
        'message': message
    }

    result = Appointments.insert_one(new_appointment)
    new_appointment['_id'] = str(result.inserted_id)
    return jsonify(data)

@app.get('/appointments')
@cross_origin(supports_credentials=True)
def get_appointments():
    print("I', here")
    print(db.find('appointments'))
    appointments = db.find('appointments')
    appointments = list(appointments)
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
    return jsonify(appointments)

# check if an future appointment exists by email or phone
@app.get('/appointment')
@cross_origin(supports_credentials=True)
def check_future_appointment():
    email = request.args.get('email')
    phone = request.args.get('phone')

    if not email and not phone:
        return jsonify({'error': 'Please provide email or phone'}), 400

    query = {}
    if email:
        query['email'] = email
    if phone:
        query['phone'] = phone

    today = datetime.today().strftime('%Y-%m-%d')
    query['date'] = {'$gte': today}

    Appointments = db.database.appointments
    future_appointments = Appointments.find(query)

    future_appointments = list(future_appointments)
    for appointment in future_appointments:
        appointment['_id'] = str(appointment['_id'])

    if future_appointments:
        return jsonify(future_appointments), 200
    else:
        return jsonify({'message': 'No future appointments found'}), 404

if __name__ == '__main__':
    app.run(port=8000)
