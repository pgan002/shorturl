# Renew Backend Code Test

## Problem

Implement a simple URL shortening web service (like [tinyurl](http://tinyurl.com/)) using the Python [Flask](http://flask.pocoo.org/docs) framework. This service will allow clients to create and delete unique identifiers for an arbitrary set of URLs and, provided a valid identifier, redirect a client to the target URL.

## Requirements

 1. Expose an endpoint to create a new shortened URL.
    * must optionally accept a user-provided ID for the shortened URL, otherwise generate one randomly
    * must not accept or generate a duplicate ID
    * must validate that IDs are non-empty and only contain alphanumeric characters
    * must include in the response a unique "authorization" token, which is different from the URL ID and may be used to delete or get additional stats about the shortened URL
    * must include in the response the shortened URL, constructed as follows: `http://{serverHostname}:{serverPort}/{urlId}`
 2. Expose an endpoint to delete an existing shortened URL.
    * must only allow deletion if the "authorization" token that was generated on creation is provided with the request
 3. Redirect valid, shortened URLs to the original full URL.
    * must keep track of successful redirects, per unique client IP address
 4. Expose an endpoint to retrieve stats about successful redirects for a shortened URL.
    * must only return stats if the "authorization" token that was generated on creation is provided with the request
    * must report counts of successful redirects per unique client IP address over the lifetime of the shortened URL

### Additional Requirements

 * Your code is expected to run on Python 3.5+.
 * You must use Flask as the web framework.
 * You are free to use any third-party Python modules that are installable via `pip`. If you do, you must add the relevant dependencies to the `requirements.txt` file.
 * You may use the provided `sqlite.py` module to interface with SQLite as your backing datastore, but you may use PostgreSQL or another relational database if you prefer. In this case, you must *write code* to setup the database schema and *document* your database configuration or any additional setup that is required to run your application.

### For bonus points

*Note: These features are completely optional - don't feel obligated to implement them!*

 * Set a default expiration time when a shortened URL is created. After the time has expired, the shortened URL should fail to redirect, and the web service should not allow further operations on the expired URL ID, but should allow a new shortened URL to be created with that ID.
 * Prevent simple DoS or brute force attacks by restricting the number of requests a particular client can make to the service within a certain timeframe.

### Example

For example, assuming a web application running on `localhost:8080`, it would support the following interaction:
```
curl -v -XPOST \
     -H"Content-type: application/json" \
     -d'{"url":"http://www.renew.com"}' \
     http://localhost:8080/create
> POST /create HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 30
> Content-Type: application/json
>
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 95
< Server: Werkzeug/0.12.2 Python/3.5.2
< Date: Thu, 12 Jan 2017 00:00:00 GMT
{"shortUrl":"http://localhost:8080/hrms3zw", "urlId":"hrms3zw", "authToken":"donjo2ef938gfo2h"}

curl -v http://localhost:8080/hrms3zw
> GET /hrms3zw HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Location: http://www.renew.com
< Server: Werkzeug/0.12.2 Python/3.5.2
< Date: Thu, 12 Jan 2017 00:00:01 GMT

curl -v -H"Authorization: donjo2ef938gfo2h" \
     http://localhost:8080/hrms3zw/stats
> GET /hrms3zw/stats HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 15
< Server: Werkzeug/0.12.2 Python/3.5.2
< Date: Thu, 12 Jan 2017 00:00:02 GMT
{"10.0.0.12":1}

curl -v -XDELETE \
     -H"Authorization: donjo2ef938gfo2h" \
     http://localhost:8080/hrms3zw
> DELETE /hrms3zw HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
>
< HTTP/1.1 204 No Content
< Server: Werkzeug/0.12.2 Python/3.5.2
< Date: Thu, 12 Jan 2017 00:00:03 GMT
```

### Endpoint Specification

**`POST /create`**

Generate and return a new, unique ID that can later be used to redirect to the provided URL. The `url` parameter must be a well-formed URL, but does not necessarily need to exist or be available.

A successful request must return with a status code `200` and a JSON object with valid `urlId`, `shortUrl`, and `authToken` values.

Otherwise, an invalid request must return with a status code `400` and a plain text error message.

##### Request
*application/json*

Body Parameters:

    url     (required - string): A well-formatted URL
    id      (optional - string): A non-empty string identifier for URL

Example:

    {
        "url": "http://www.renew.com"
    }

##### Responses
Status `200` (success): *application/json*

    {
        "shortUrl": "string",
        "urlId": "string",
        "authToken": "string"
    }

Status `400` (error):

    Error Message
---
**`GET /{urlId}`**

Given a valid `urlId`, redirect the client to the target URL with a status code `301`.

An invalid request must return with a status code `404` and a plain text error message.

##### Responses
Status `301` (success)

Status `404` (error):

    Error Message
---
**`GET /{urlId}/stats`**

Given a valid `urlId`, return with a status code `200` and a JSON object with numeric counts of successful redirects, per unique client IP address.

A request with a missing or incorrect `authToken` must return with a status code `403` and a plain text error message.

An invalid request must return with a status code `404` and a plain text error message.

##### Request

Request Headers:

    Authorization  (required - string): The authToken associated with the urlId

##### Responses
Status `200` (success): *application/json*

    {
        "ip_address_1": int,
        "ip_address_2": int,
        ...
    }

Status `403` (error):

    Error Message

Status `404` (error):

    Error Message
---
**`DELETE /{urlId}`**

Given a valid `urlId`, remove the mapping to the target URL. A subsequent `GET` request with the `urlId` should yield a `404` response.

A request with a missing or incorrect `authToken` must return with a status code `403` and a plain text error message.

An invalid request must return with a status code `404` and a plain text error message.

##### Request

Request Headers:

    Authorization  (required - string): The authToken associated with the urlId

##### Responses
Status `204` (success)

Status `403` (error):

    Error Message

Status `404` (error):

    Error Message

## Project Structure
The following modules are provided for you as a starting point for your web application:

```
.
├── README.md
├── requirements.txt
├── run.py
└── src
    └── db
        ├── __init__.py
        └── sqlite.py
    ├── __init__.py
    └── routes.py
```

You may modify any of the provided application code and define new modules and/or functions *as long as* your application starts a webserver bound to port `8080` on `localhost` and is runnable via the following command from the top-level directory:

`python -m run`

### Modules
`run.py`

Imports the routes module and runs the webserver on `localhost:8080`. You can run the webserver from the top-level directory with the following command: `python -m run`

`src/__init__.py`

The Flask application object is initialized in this file.

`src/routes.py`

Module where the routes, as specified in the `Endpoint Specification` section, are defined - these are the functions that you must implement.

`src/db/sqlite.py`

Module providing a simple wrapper around an `sqlite3` database connection. You are free to use this module as-is, modify it, or ignore it.
