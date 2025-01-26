// server.js
const express = require('express');
const mongoose = require('mongoose');

// If you prefer environment variables, install dotenv and do:
// require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON from incoming requests
app.use(express.json());

// --- 1) Connect to MongoDB Atlas ---

const uri = 'mongodb+srv://as7108:EgqPUvQ1xhoAHZkp@microwet.pjzpl.mongodb.net/';

mongoose
  .connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    console.log('Connected to MongoDB Atlas');
  })
  .catch((err) => {
    console.error('Error connecting to MongoDB Atlas:', err);
  });

// --- 2) Define a Mongoose schema/model for sensor data ---

// define the variables that the esp32 is sending------------------------
const sensorDataSchema = new mongoose.Schema({
  //deviceId: String,
  temperature: Number,
  //humidity: Number,
  timestamp: { type: Date, default: Date.now },
  // add fields that match the JSON you send from the ESP32
});

const SensorData = mongoose.model('SensorData', sensorDataSchema);

// --- 3) Set up the POST endpoint to handle ESP32 data ---
app.post('/data', async (req, res) => {
  try {
    // req.body is the JSON data from the ESP32
    const sensorData = new SensorData(req.body);

    // Save data in the DB
    await sensorData.save();

    console.log('Received data:', sensorData);
    return res.status(201).json({ message: 'Data saved successfully' });
  } catch (error) {
    console.error('Error saving data:', error);
    return res.status(500).json({ error: 'Failed to save data' });
  }
});

// --- 4) Start the server ---
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
