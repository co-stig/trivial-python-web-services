#! /usr/bin/env python

#from wsgiref.simple_server import make_server

from vsws import url_pattern, Controller
from webob import Request, Response

@url_pattern("/users")
def get_users ():
	return "Inside get_users()"

@url_pattern("/users/${username}")
def get_user (username):
	return "Inside get_user('%s')" % username

@url_pattern("/users/${username}/plans")
def get_plans (username):
	return "Inside get_plans('%s')" % username

@url_pattern("/users/${username}/plans/${year}")
def get_plan (username, year, method, param2 = ''):
	return "Inside get_plan('%s', %s, %s, %s)" % (username, year, method, param2)


#make_server('localhost', 8051, Controller()).handle_request()

print Request.blank ('/users/kostya/plans/2009?param1=aa&param2=bb&param1=cc').get_response (Controller())
