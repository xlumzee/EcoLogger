/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('mongodbVSCodePlaygroundDB');


db.getCollection('WeatherData').insertMany(
[{"sensorid": "sensor-001",
  "temperature": 22,
  "humidity": 50,
  "latitude": 11,
  "longitude": 70,
  "timestamp": ISODate("2025-01-01T10:30:00Z")},

  {"sensorid": "sensor-002",
    "temperature": 22,
    "humidity": 50,
    "latitude": 11,
    "longitude": 70,
    "timestamp": ISODate("2025-01-01T10:30:00Z")},

   {"sensorid": "sensor-003",
    "temperature": 22,
    "humidity": 50,
    "latitude": 11,
    "longitude": 70,
    "timestamp": ISODate("2025-01-01T10:30:00Z")}, 

]);


// 1. Count how many readings occurred on Jan 1st, 2025.
const readingsOnJan1 = db.getCollection('WeatherData').find({
  timestamp: {
    $gte: new Date('2025-01-01T00:00:00Z'),
    $lt: new Date('2025-01-02T00:00:00Z')
  }
}).count();

console.log(`${readingsOnJan1} readings occurred on January 1st, 2025.`);

