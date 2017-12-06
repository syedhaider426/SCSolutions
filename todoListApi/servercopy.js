/* Node.js Web Server setup and port listening */

var express = require('express'),
    app = express(), //http application using express
    secureApp = express(), //secure https application using express
    http = require('http'),
    https = require('https'),
    port = process.env.PORT || 3000,
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

const YEAR = 31536000000; //year to milliseconds

//set up secure https application using helmet (sets HTTP headers)
secureApp.use(h.hsts({
    maxAge: YEAR,
    includeSubdomains: true,
    force: true
}));
var cipher = ['ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-CBC-SHA384',
    'ECDHE-RSA-AES256-CBC-SHA256',
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'DHE-RSA-AES128-GCM-SHA256',
    'DHE-RSA-AES256-GCM-SHA384',
    '!aNULL',
    '!MD5',
    '!DSS'].join(':');

//parses URL-encoded data with qs library option (because extended: true)
app.use(bodyParser.urlencoded({ extended: true }));
secureApp.use(bodyParser.urlencoded({ extended: true })); 

app.use(bodyParser.json());
secureApp.use(bodyParser.json());

//var publicKey = reader.readFileSync('/home/syed/yourkeyname.pem','utf8'); //reads public key with encoding

//creating (stateless) jwt for user session
//secureApp.use(jwt({ secret: publicKey }).unless({ path: ['/sign_in', '/register', '/loginRequired'] }));

var routes = require('./api/routes/todoListRoutes'); //importing route
routes(secureApp); //register the route
routes(app);

//information necessary for 
var ops = {
    key: reader.readFileSync('/etc/letsencrypt/live/chatwithme.me/privkey.pem'),
    cert: reader.readFileSync('/etc/letsencrypt/live/chatwithme.me/fullchain.pem'),
    ciphers: cipher
};
//Instance server for http and https Node.js web application
http.createServer(app).listen(port);
https.createServer(ops, secureApp).listen(port);

console.log('todo list RESTful API server started on: ' + port);
