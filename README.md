# Very simple Python RESTful web services #

It's just a single-100-LOC-file (see [vsws.py](https://github.com/co-stig/python-very-simple-web-services/blob/master/vsws.py)), allowing you to create RESTful web services in a very simple manner through a `@url_pattern` decorator. It might be useful for simple projects, prototypes, etc. 

Why would you use it? Well, it's just two pages of code, which means it's very light and there are fewer things to go wrong. Also, if you found a bug or want to extend the functionality -- you can do it yourself in the blink of an eye.

Last time I tested this code, I used Python 3.4 on Windows 8.1 64 bit with WebOb 1.4.

Sample code:

```python
#! /usr/bin/env python

from vsws import url_pattern, Controller
from webob import Request, Response
from wsgiref.simple_server import make_server

# You can specify multiple URL patterns for a single handler and use response object for better control
@url_pattern("/users")
@url_pattern("/all_users")
@url_pattern("/users/${username}/list", ['GET'])
def get_users (response):
	response.status = 200
	return "Inside get_users()"

# Returning a dict corresponding to HTTP resoponse -- less control, but simpler
@url_pattern("/users/${username}")
def get_user (username):
	return {"body": "Inside get_user('%s')" % username, "status": 201}

# Handling both GET and PUT requests and returning a simple string, HTTP 200 is used by default
@url_pattern("/users/${username}/plans", ['GET', 'PUT'])
def get_plans (username):
	return "Inside get_plans('%s'), GET or PUT" % username

# POST request with the same URL pattern can be handled separately
@url_pattern("/users/${username}/plans", ['POST'])
def get_plans (username):
	return "Inside get_plans('%s'), POST" % username

# Here param2 is a request parameter, i.e. /users/john/plans/2015?param2=test
# method is either GET, POST, PUT or DELETE
@url_pattern("/users/${username}/plans/${year}")
def get_plan (username, year, method, param2 = ''):
	return "Inside get_plan('%s', %s, %s, %s)" % (username, year, method, param2)

# Uncomment this to line to actually start a server:
# make_server('localhost', 8051, Controller()).serve_forever()

print (Request.blank ('/users/john/plans/2009?param1=value1&param2=value2').get_response (Controller()))
```

# Installation and requirements #

Just copy vsws.py to your project root.

As for now, it requires WebOb, though can be easily adapted for a plain WSGI usage. When I say "easily", I mean in 30 minutes or so.

In Python 3.4 installing WebOb is as simple as executing `pip install webob`

# Usage #

  1. Import Decorator and Controller: `from vsws import url_pattern, Controller`
  1. Design an URL, including all the necessary parameters: `/users/${username}/plans/${year`}
  1. Create a function, taking the same parameters (`username` and `year` in this case)
  1. Add a decorator for this function: `@url_pattern("/users/${username}/plans/${year}")`
  1. Use `Controller()` as an WSGI Application: `make_server('localhost', 8051, Controller()).serve_forever()`

## Features ##

  1. URL handler can return both plain text (in this case it becomes a response body), or `dict`, which can contain any of the following:
    1. `body`
    1. `status`
    1. `charset`
    1. `content_type`
    1. `additional_headers`
  1. URL handler decorator has two arguments:
    1. `url_pattern`
    1. `methods = ['GET', 'PUT', 'POST', 'DELETE']`
  1. Request parameters and those extracted using the URL pattern are handled in the same way, so that you can have handlers like this: `def my_handler (username, age = '')` decorated with `username` as a part of URL: `@url_pattern("/users/${username}")`, and `age` will be taken from the request parameters transparently, e.g. `http://localhost/users/john?age=30`.
  1. There are few additional parameters, also handled in the same way:
    1. `request`: WebOb Request
    1. `response`: WebOb Response
    1. `method`: method (GET / POST / PUT / DELETE)
    1. `headers`
  1. The URL handler can have less parameters than provided by request and extracted using URL pattern. In such case those parameters are not used.
  1. If there exist some mandatory (not having default values) URL handler parameters, which are not supplied during the request (not enough parameters), `400 Bad Request` is returned.
  1. Trailing slashes in URLs are ignored: `http://localhost/users` is equivalent to `http://localhost/users/`.
  1. You can use several decorators for a single URL handler.

## Limitations ##

  1. URL handlers should be static.
  1. Several request parameters with the same name are not supported (only one of those will be used). Think of radiobutton groups.
  1. Varargs in handlers are not supported.
  1. `400 Bad Request` is thrown even if URL matches, but the method is not supported (should be `405 Method Not Allowed` instead).
  1. Parameter name can't be one of the following: `request`, `response`, `method`, `headers`. Those are special "reserved" parameters used internally.

## Defaults ##

  1. Content-Type: text/plain
  1. Status: 200 OK
