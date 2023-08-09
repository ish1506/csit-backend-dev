from datetime import datetime

from flask import Flask, request
from flask_api import status
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/')
db = client.minichallenge


@app.route('/flight', methods=['GET'])
def flights():
    args = request.args
    departure_date = args.get('departureDate')
    return_date = args.get('returnDate')
    destination = args.get('destination')

    if not (departure_date and return_date and destination):
        return 'Bad input', status.HTTP_400_BAD_REQUEST

    try:
        iso_departure = datetime.fromisoformat(departure_date)
        iso_return = datetime.fromisoformat(return_date)
    except ValueError as e:
        return 'Bad input', status.HTTP_400_BAD_REQUEST
    
    q1 = {
        'srccity': 'Singapore',
        'destcity': destination,
        'date': iso_departure,
    }
    q2 = {
        'srccity': destination,
        'destcity': 'Singapore',
        'date': iso_return,
    }
 
    collection = db.flights
    flights_there = collection.find(q1).sort('price', 1)
    flights_back = collection.find(q2).sort('price', 1)

    cheapest_dep_flights = []
    cheapest_ret_flights = []

    prev_price = None
    for f in flights_there:
        airline = f['airline']
        price = f['price']
        
        # This is only true when initialising prev_price (ie first item in Cursor) 
        if not prev_price:
            prev_price = price
        if price > prev_price:
            break
        cheapest_dep_flights.append({
            'Departure Airline': airline,
            'Departure Price': price,
        })
    if not cheapest_dep_flights:
        return [], status.HTTP_200_OK
    
    prev_price = None
    for f in flights_back:
        airline = f['airline']
        price = f['price']
        
        # This is only true when initialising prev_price (ie first item in Cursor)
        if not prev_price:
            prev_price = price
        if price > prev_price:
            break
        cheapest_ret_flights.append({
            'Return Airline': airline,
            'Return Price': price,
        })
    if not cheapest_ret_flights:
        return [], status.HTTP_200_OK

    cheapest_flights = []
    for cdf in cheapest_dep_flights:
        for crf in cheapest_ret_flights:
            cheapest_flights.append({
                'City': destination,
                'Departure Date': departure_date,
                'Departure Airline': cdf['Departure Airline'],
                'Departure Price': cdf['Departure Price'],
                'Return Date': return_date,
                'Return Airline': crf['Return Airline'],
                'Return Price': crf['Return Price'],
            })

    return cheapest_flights, status.HTTP_200_OK


@app.route('/hotel/', methods=['GET'])
def hotels():
    args = request.args
    checkin_date = args.get('checkInDate')
    checkout_date = args.get('checkOutDate')
    destination = args.get('destination')

    if not (checkin_date and checkout_date and destination):
        return 'Bad input', status.HTTP_400_BAD_REQUEST

    try:
        iso_checkin = datetime.fromisoformat(checkin_date)
        iso_checkout = datetime.fromisoformat(checkout_date)
    except ValueError as e:
        return 'Bad input', status.HTTP_400_BAD_REQUEST

    q = {
        'city': destination,
        'date': {
            '$gte': iso_checkin,
            '$lte': iso_checkout,
        },
    }
    pipeline = [
        {
            '$match': q
        },
        {
            '$group': {
                '_id': '$hotelName',
                'totalPrice': {'$sum': '$price'}
            },
        },
        {
            '$sort': {
                'totalPrice': 1
            }
        },
    ]

    collection = db.hotels
    aggregated_query = collection.aggregate(pipeline)

    hotels = []
    prev_price = None
    for h in aggregated_query:
        hotel = h['_id']
        price = h['totalPrice']

        # This is only true when initialising prev_price (ie first item in Cursor)
        if not prev_price:
            prev_price = price
        if price > prev_price:
            break
        hotels.append({
            'City': destination,
            'Check In Date': checkin_date,
            'Check Out Date': checkout_date,
            'Hotel': hotel,
            'Price': price,
        })

    return hotels, status.HTTP_200_OK


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)