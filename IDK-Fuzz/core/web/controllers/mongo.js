const mongoose = require('mongoose');
const Schema = mongoose.Schema;

mongoose.Promise = global.Promise;

const jobSchema = new Schema({
    active: Boolean,
    jobName: String,
    binName: String,
    imageName: String,
    author: String,
    mcount: Number,
    fcount: Number,
    testCases: Number,
    startDate: String,
    startTime: String
});
const Jobs = mongoose.model('jobs', jobSchema);

/* first is the db name */
mongoose.connect("mongodb://localhost/first");
mongoose.connection.once('open', function () {
    console.log("Success! Conencted to db");
}).on('error', function (err) {
    console.log("Erro! Could not connect to db");
});

module.exports.Save = function (data) {
    let date = new Date();
    let job = new Jobs({
        active: true,
        jobName: data.bname,
        binName: data.bname,
        imageName: data.iname,
        author: data.aname,
        mcount: data.mcount,
        fcount: data.fcount,
        testCases: 0,
        startDate: date.toLocaleDateString(),
        startTime: date.toLocaleTimeString()
    });

    job.save().then(function () {
        if (job.isNew) {
            console.log("Error! Could not insert into db");
        }
        else {
            console.log("Success! Added new entry to db");
        }
    });
};

module.exports.findAll = async function () {
    let active = [];
    let inactive = [];
    let records = await Jobs.find({}).then(function (res) {
        for (let i = 0; i < res.length; i++) {
            if (res[i].active) {
                active.push({ name: res[i].author, jobname: res[i].jobName });
            }
            else {
                inactive.push({ name: res[i].author, jobname: res[i].jobName });
            }
        }
    });
    return { active: active, inactive: inactive };
};

module.exports.findItem = async function(jname){
    let item = {};
    await Jobs.find({jobName: jname}).then(function(res){
        item = res;
    });
    return item[0];
};