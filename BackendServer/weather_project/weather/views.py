
# Create your views here.
from django.http import JsonResponse
from pymongo import MongoClient
import json

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://as7108:<db_password>@microwet.pjzpl.mongodb.net/weatherdb?retryWrites=true&w=majority")

db = client.weatherdb
collection = db.WeatherData

def save_sensor_data(request):
    if request.method == 'POST':
        # Assuming data is being sent as JSON
        data = json.loads(request.body)
        sensor_data = {
            'sensorid': data.get('sensorid'),
            'temperature': data.get('temperature'),
            'humidity': data.get('humidity'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timestamp': data.get('timestamp')
        }

        # Insert into MongoDB
        collection.insert_one(sensor_data)

        return JsonResponse({"message": "Data received and stored successfully."}, status=200)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
