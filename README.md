# Python Flask: Stock Trades API

## Project Specifications

**Read-Only Files**
- tests/*

**Commands**
- run:
```bash
source env1/bin/activate && flask --app app init-db && flask --app app run -p 8000
```
- test:
```bash
source env1/bin/activate && python -m pytest --junitxml=unit.xml
```

## Question description

In this challenge, your task is to implement a simple REST API to manage a collection of stock trades.

Each trade has the following structure:

- `id`: The unique ID of the trade. (Integer)
- `type`: The type of the trade, either 'buy' or 'sell'. (String)
- `user_id`: The unique user ID. (Integer)
- `symbol`: The stock symbol of the trade. (String)
- `shares`: The total number of shares traded. The traded shares value is between 10 and 30 shares, inclusive. (Integer)
- `price`: The price of one share of stock at the time of the trade. (Integer)
- `timestamp`: The epoch time of the stock trade in milliseconds. (Integer)


### Example of a trade data JSON object:
```
{
    "id": 1,
    "type": "buy",
    "user_id": 23,
    "symbol": "ABX",
    "shares": 30,
    "price": 134,
    "timestamp": 1531522701000
}
```

## Requirements:

You are provided with the implementation of the Trade model. The REST service must expose the `/trades` endpoint, which allows for managing the collection of trade records in the following way:

`POST /trades`:

- creates a new trade
- expects a JSON trade object without an id property as a body payload. You can assume that the given object is always valid.
- adds the given trade object to the collection of trades and assigns a unique integer id to it. The first created trade must have id 1, the second one 2, and so on.
- the response code is 201, and the response body is the created trade object

`GET /trades`:

- returns a collection of all trades
- the response code is 200, and the response body is an array of all trade objects ordered by their ids in increasing order

`GET /trades/<id>`:

- returns a trade with the given id
- if the matching trade exists, the response code is 200 and the response body is the matching trade object
- if there is no trade with the given id in the collection, the response code is 404

`DELETE`, `PUT`, `PATCH` request to `/trades/<id>`:

- the response code is 405 because the API does not allow deleting or modifying trades for any id value


## Environment
