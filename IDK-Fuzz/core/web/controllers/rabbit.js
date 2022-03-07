const amqp = require('amqplib/callback_api');
var count = 0;

module.exports = function (data) {
    amqp.connect('amqp://localhost', function (error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function (error1, channel) {
            if (error1) {
                throw error1;
            }
            var queue = 'task-queue';

            channel.assertQueue(queue, {
                durable: true
            });

            var msg = {
                "FuzzNo": count,
                "appName": data.bname,
                "mcount": data.mcount,
                "fcount": data.fcount,
                "fImage": data.iname + ':latest',
                "mImage": ""
            };

            channel.sendToQueue(queue, Buffer.from(JSON.stringify(msg)));
            count++;
            console.log("Success! Entry inserted into queue");
        });
    });
};
