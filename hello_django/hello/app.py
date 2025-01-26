from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Flask app setup
app = Flask(__name__)

# MongoDB connection URI and database/collection details
MONGO_URI = "mongodb+srv://as7108:EgqPUvQ1xhoAHZkp@microwet.pjzpl.mongodb.net/"
DATABASE_NAME = "mongodbVSCodePlaygroundDB"
COLLECTION_NAME = "WeatherData"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test connection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    logging.info("Connected to MongoDB Atlas successfully!")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    collection = None


@app.route('/')
def dashboard():
    """Render the main dashboard."""
    return render_template('hello/index.html')


@app.route('/latest-data')
def latest_data():
    """Fetch the latest weather data as JSON."""
    # Default fallback data
    latest_data = {
        "sensorid": "N/A",
        "temperature": "N/A",
        "humidity": "N/A",
        "latitude": "N/A",
        "longitude": "N/A",
        "timestamp": "N/A"
    }

    if collection is not None:
        try:
            # Fetch the latest document based on the timestamp
            latest_data = collection.find_one(sort=[("timestamp", -1)]) or latest_data
            logging.info(f"Latest data retrieved: {latest_data}")
        except Exception as e:
            logging.error(f"Error retrieving data from MongoDB: {e}")

    # Format the data to be JSON-serializable
    formatted_data = {
        "sensorid": latest_data.get("sensorid", "N/A"),
        "temperature": latest_data.get("temperature", "N/A"),
        "humidity": latest_data.get("humidity", "N/A"),
        "position": f"({latest_data.get('latitude', 'N/A')}, {latest_data.get('longitude', 'N/A')})",
        "timestamp": str(latest_data.get("timestamp", "N/A"))
    }

    return jsonify(formatted_data)


@app.route('/test-db')
def test_db():
    """Test route to display all documents in the collection."""
    if collection is not None:
        try:
            all_data = list(collection.find())  # Fetch all documents
            return jsonify(all_data)
        except Exception as e:
            logging.error(f"Error fetching data from MongoDB: {e}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No connection to MongoDB."}), 500


if __name__ == '__main__':
    app.run(debug=True)
