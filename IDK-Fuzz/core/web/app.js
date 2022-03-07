const express = require('express');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const rabbit = require('./controllers/rabbit');
const mongo = require('./controllers/mongo');

var app = express();
app.set('view engine', 'ejs');
app.use('/assets', express.static('assets'));
app.use('/scripts', express.static('scripts'));
app.use(fileUpload());

var urlEncodedParser = bodyParser.urlencoded({ extended: false });

app.post('/stats', urlEncodedParser,async function (req, res) {
    let binary = req.files.bin;
    let path = __dirname + "/uploads/" + binary.name;

    binary.mv(path, function (err) { if (err) throw err; });

    rabbit(req.body);
    mongo.Save(req.body);

    let items = await mongo.findAll();
    res.render('stats.ejs', {data: items});
});

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.get('/stats', async function (req, res) {
    let items = await mongo.findAll();
    res.render('stats.ejs', {data: items});
});

app.get('/details/',async function (req, res) {
    let item = await mongo.findItem(req.query.name);
    res.render('details', {details: item});
});

app.listen(1337);