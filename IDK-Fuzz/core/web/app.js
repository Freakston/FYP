var express = require('express');
var bodyParser = require('body-parser');
var fileUpload = require('express-fileupload');

var app = express();
app.set('view engine','ejs');
app.use('/assets', express.static('assets'));
app.use('/scripts', express.static('scripts'));
app.use(fileUpload());

var urlEncodedParser = bodyParser.urlencoded({extended: false});

app.post('/stats', urlEncodedParser, function (req, res){
    console.log(req.body);
    let binary = req.files.bin;
    let path = __dirname+"/uploads/"+binary.name;

    binary.mv(path, function(err){
        if(err) throw err;
    });

    res.sendFile(__dirname + '/stats.html');
});

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});

app.get('/stats', function(req, res){
    res.sendFile(__dirname + '/stats.html');
});

app.get('/details/', function(req, res){
    console.log(req.query);
    res.render('details', {name: req.query.name});
});


app.listen(1337);