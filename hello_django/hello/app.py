from flask import Flask, render_template, jsonify, request
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
            latest_data = collection.find_one(sort=[("timestamp", -1)]) or latest_data
            logging.info(f"Latest data retrieved: {latest_data}")

            if "timestamp" in latest_data:
                raw_timestamp = latest_data["timestamp"]
                try:
                    epoch_time = float(raw_timestamp)
                    human_readable_time = datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    human_readable_time = "Invalid timestamp format"

                latest_data["timestamp"] = human_readable_time
            else:
                latest_data["timestamp"] = "N/A"

        except Exception as e:
            logging.error(f"Error retrieving data from MongoDB: {e}")

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


@app.route('/historical-data')
def historical_data():
    """Fetch the last X records for historical data visualization."""
    try:
        # Get the number of data points from the query parameter
        points = int(request.args.get('points', 50))

        # Fetch data sorted by timestamp in descending order and limit to `points`
        cursor = collection.find().sort("timestamp", -1).limit(points)
        records = list(cursor)

        # Reverse the order so the newest data is on the right (chronological order)
        historical_records = []
        for record in reversed(records):
            try:
                epoch_time = float(record.get("timestamp", "0"))
                human_readable_time = datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                human_readable_time = "Invalid timestamp format"

            historical_records.append({
                "timestamp": human_readable_time,
                "temperature": record.get("temperature", "N/A"),
                "humidity": record.get("humidity", "N/A")
            })

        return jsonify(historical_records)

    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        return jsonify({"error": "Failed to fetch historical data."}), 500


@app.route('/test-db')
def test_db():
    """Test route to display all documents in the collection."""
    if collection is not None:
        try:
            all_data = list(collection.find())
            return jsonify(all_data)
        except Exception as e:
            logging.error(f"Error fetching data from MongoDB: {e}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No connection to MongoDB."}), 500


if __name__ == '__main__':
    app.run(debug=True)