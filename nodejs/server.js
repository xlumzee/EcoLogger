// server.js
const express = require('express');
const mongoose = require('mongoose');

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON from incoming requests
app.use(express.json());

// 1) Connect to MongoDB Atlas
// - Add your desired database name after the slash below (e.g., /myDatabase)
const uri = 'mongodb+srv://as7108:EgqPUvQ1xhoAHZkp@microwet.pjzpl.mongodb.net/?retryWrites=true&w=majority';

mongoose
  .connect(uri)
  .then(() => {
    console.log('Connected to MongoDB Atlas');
  })
  .catch((err) => {
    console.error('Error connecting to MongoDB Atlas:', err);
  });

// 2) Define a Mongoose schema/model for sensor data
//    The ESP sends: { "Time": "1/25/2025 20:17:54", "Temperature": "24.34" }
const sensorDataSchema = new mongoose.Schema({
  timestamp: Date,    // We'll store "Time" as a Date
  temperature: Number // We'll store "Temperature" as a Number
});

const SensorData = mongoose.model('SensorData', sensorDataSchema);

// 3) POST endpoint to handle ESP data
app.post('/data', async (req, res) => {
  try {
    // Example incoming JSON:
    // { "Time": "1/25/2025 20:17:54", "Temperature": "24.34" }
    const rawTime = req.body.Time;
    const rawTemperature = req.body.Temperature;

    // Convert incoming strings to the correct types
    const timestamp = new Date(rawTime);
    const temperature = parseFloat(rawTemperature);

    // Create a new document
    const sensorData = new SensorData({
      timestamp,
      temperature
    });

    // Save to the database
    await sensorData.save();

    console.log('Received data:', sensorData);
    return res.status(201).json({ message: 'Data saved successfully' });
  } catch (error) {
    console.error('Error saving data:', error);
    return res.status(500).json({ error: 'Failed to save data' });
  }
});

// 4) Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
