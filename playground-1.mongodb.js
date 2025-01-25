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

// Insert a few documents into the sales collection.
// db.getCollection('WeatherData').insertMany([
//   { 'item': 'abc', 'price': 10, 'quantity': 2, 'date': new Date('2014-03-01T08:00:00Z') },
//   { 'item': 'jkl', 'price': 20, 'quantity': 1, 'date': new Date('2014-03-01T09:00:00Z') },
//   { 'item': 'xyz', 'price': 5, 'quantity': 10, 'date': new Date('2014-03-15T09:00:00Z') },
//   { 'item': 'xyz', 'price': 5, 'quantity': 20, 'date': new Date('2014-04-04T11:21:39.736Z') },
//   { 'item': 'abc', 'price': 10, 'quantity': 10, 'date': new Date('2014-04-04T21:23:13.331Z') },
//   { 'item': 'def', 'price': 7.5, 'quantity': 5, 'date': new Date('2015-06-04T05:08:13Z') },
//   { 'item': 'def', 'price': 7.5, 'quantity': 10, 'date': new Date('2015-09-10T08:43:00Z') },
//   { 'item': 'abc', 'price': 10, 'quantity': 5, 'date': new Date('2016-02-06T20:20:13Z') },
// ]);

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

