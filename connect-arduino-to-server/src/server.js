const express = require('express');
const mongoose = require('mongoose');

// Connect to MongoDB
let db_url = "mongodb://localhost/my_database"
mongoose.connect(db_url);

// Define your data schema
const DataSchema = new mongoose.Schema({
  value: Number,
  timestamp: Date
});
const DataModel = mongoose.model('Data', DataSchema);

// Set up Express
const app = express();
app.use(express.json());

// Endpoint to receive data from Arduino
app.post('/data', (req, res) => {
  const newData = new DataModel(req.body);
  newData.save()
    .then(() => res.sendStatus(200))
    .catch(err => res.status(500).send(err));
});

app.listen(3000);
