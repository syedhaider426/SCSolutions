/* Node.js Web Server setup and port listening */

var express = require('express'),
    app = express(), //http application using express
    secureApp = express(), //secure https application using express
    http = require('http'),
    https = require('https'),
    port = process.env.PORT || 3000,
    httpPort = process.env.PORT || 8080
    mongoose = require('mongoose'),
    Task = require('./api/models/todoListModel'), //created model loading here
    User = require('./api/models/userModel'),
    jwt = require('express-jwt'),
    reader = require('fs'),
    h = require('helmet'),
    bodyParser = require('body-parser');
  
// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/Tododb', { useMongoClient: true }); //allows for client connection

