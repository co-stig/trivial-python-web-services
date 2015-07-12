#! /usr/bin/env python
#
# Trivial Python Web Services sample
#
# https://github.com/co-stig/trivial-python-web-services
#
# Copyright (C) Constantine Kulak, 2009 -- 2015
#

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