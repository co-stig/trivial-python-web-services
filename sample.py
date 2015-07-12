#! /usr/bin/env python

from vsws import url_pattern, Controller
from webob import Request, Response
from wsgiref.simple_server import make_server

@url_pattern("/users")
@url_pattern("/all_users")
@url_pattern("/users/${username}/list", ['GET'])
def get_users (response):
	response.status = 200
	return "Inside get_users()"

@url_pattern("/users/${username}")
def get_user (username):
	return {"body": "Inside get_user('%s')" % username, "status": 201}

@url_pattern("/users/${username}/plans", ['GET', 'PUT'])
def get_plans (username):
	return "Inside get_plans('%s'), GET or PUT" % username

@url_pattern("/users/${username}/plans", ['POST'])
def get_plans (username):
	return "Inside get_plans('%s'), POST" % username

@url_pattern("/users/${username}/plans/${year}")
def get_plan (username, year, method, param2 = ''):
	return "Inside get_plan('%s', %s, %s, %s)" % (username, year, method, param2)

# Uncomment this to line to actually start a server:
# make_server('localhost', 8051, Controller()).serve_forever()

#print (Request.blank ('/users/john/plans/2009?param1=value1&param2=value2').get_response (Controller()))