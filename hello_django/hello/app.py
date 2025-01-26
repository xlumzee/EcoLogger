from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
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

            # Convert timestamp to human-readable format
            if "timestamp" in latest_data:
                raw_timestamp = latest_data["timestamp"]

                # Check and handle different formats
                try:
                    # Case 1: ISO 8601 format string
                    human_readable_time = datetime.fromisoformat(raw_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    try:
                        # Case 2: Custom format string (e.g., '2025/01/25 15:30:00')
                        human_readable_time = datetime.strptime(raw_timestamp, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        try:
                            # Case 3: Epoch time (int or string)
                            epoch_time = float(raw_timestamp)  # Ensure it's a float for seconds
                            human_readable_time = datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
                        except (ValueError, TypeError):
                            # Case 4: Invalid or unrecognized format
                            human_readable_time = "Invalid timestamp format"

                latest_data["timestamp"] = human_readable_time
            else:
                latest_data["timestamp"] = "N/A"

        except Exception as e:
            logging.error(f"Error retrieving data from MongoDB: {e}")

    # Format the data to be JSON-serializable
    formatted_data = {
        "sensorid": latest_data.get("sensorid", "N/A"),
        "temperature": latest_data.get("temperature", "N/A"),
        "humidity": latest_data.get("humidity", "N/A"),
        "position": f"({latest_data.get('latitude', 'N/A')}, {latest_data.get('longitude', 'N/A')})",
        "latitude": latest_data.get("latitude", "N/A"),
        "longitude": latest_data.get("longitude", "N/A"),
        "timestamp": latest_data.get("timestamp", "N/A")
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
