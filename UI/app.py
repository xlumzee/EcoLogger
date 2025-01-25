import streamlit as st
import pymongo
from datetime import datetime

# 1. Connect to your MongoDB (Atlas or local)

client = pymongo.MongoClient("mongodb+srv://as7108:<db_password>@microwet.pjzpl.mongodb.net/")
db = client["weatherdb"]
collection = db["WeatherData"]

# 2. Streamlit UI setup
st.title("Temperature Dashboard")

# 3. Fetch some data
docs = collection.find().sort("timestamp", -1)  # Sort by timestamp DESC
docs_list = list(docs)  # Convert cursor to list

if not docs_list:
    st.write("No documents found in WeatherData.")
else:
    # 4. Display the temperature from the most recent document
    latest_doc = docs_list[0]
    st.metric("Most Recent Temperature (°C)", latest_doc["temperature"])

    # 5. (Optional) Show all documents in a table (or any format you like)
    #    We'll extract temperature, humidity, timestamp, etc.
    data_to_display = [
        {
            "sensorid": d["sensorid"],
            "temperature": d["temperature"],
            "humidity": d["humidity"],
            "timestamp": d["timestamp"]
        }
        for d in docs_list
    ]

    st.write("All Retrieved Documents")
    st.table(data_to_display)
