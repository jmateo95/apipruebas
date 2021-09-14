const express = require('express');
const app = express();
const port = 3000;

const respone={
    "rates": [
        {
            "service_name": "canadapost-overnight",
            "service_code": "ON",
            "total_price": "1295",
            "description": "This is the fastest option by far",
            "currency": "CAD",
            "min_delivery_date": "2013-04-12 14:48:45 -0400",
            "max_delivery_date": "2013-04-12 14:48:45 -0400"
        },
        {
            "service_name": "fedex-2dayground",
            "service_code": "2D",
            "total_price": "2934",
            "currency": "USD",
            "min_delivery_date": "2013-04-12 14:48:45 -0400",
            "max_delivery_date": "2013-04-12 14:48:45 -0400"
        },
        {
            "service_name": "fedex-priorityovernight",
            "service_code": "1D",
            "total_price": "3587",
            "currency": "USD",
            "min_delivery_date": "2013-04-12 14:48:45 -0400",
            "max_delivery_date": "2013-04-12 14:48:45 -0400"
        }
    ]
};


app.get('/', (req, res) => res.send('Hello World!'));

app.get('/hola', (req, res) => res.send(respone));

// Endpoint to Get a list of users
app.get('/getUsers', function(req, res){
    res.send(respone)
})

app.listen(process.env.PORT || port, () => console.log(`Example app listening at http://localhost:${port}`));