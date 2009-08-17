#! /usr/bin/env python

from webob import Request, Response
import re
import inspect

# Limitations: 
# Handlers should be static
# Several request parameters with the same name are not supported (only one will be used)
# handler varargs are not supported

# Defaults:
# Content-Type: text/plain
# 200 OK

# Special arguments:
# request: WebOb Request
# response: WebOb Response
# method: method (GET / POST / PUT / DELETE)
# headers

# Return dict elements:
# body
# charset
# content_type
# additiona_headers
# status

# done: Return dict / string
# done: Method as a parameter
# done: Several URLs
# done: Error (HTTP 400) if handler has more *required* arguments than supplied

class UrlCallableFunction (object):
	
	param_re = re.compile(r'\$\{(.+?)\}')
	request_handlers = []
	
	def __init__ (self, func, pattern, methods):
		self.pattern = pattern
		self.func = func
		self.param_names = UrlCallableFunction.param_re.findall(pattern)
		self.re = '^' + UrlCallableFunction.param_re.sub('([^/]+?)', pattern) + '$'
		self.re_compiled = re.compile(self.re)
		self.methods = methods
		
	def call_if_matches (self, url, additional_params):
		if additional_params['method'] in self.methods:
			match = self.re_compiled.findall (url)
			if match:
				# A trick for more than one group
				if not isinstance (match[0], str):
					match = list(match[0])
					
				# Combine pattern parameter names and actual values from URL,
				# append additional_params and leave only those present in handler's signature
				params = dict(zip(self.param_names, match))
				params.update(additional_params)
				real_args = inspect.getargspec(self.func).args
				diff = filter(lambda x: x not in real_args, params.keys())
				for arg in diff:
					del params[arg]
				
				# Check if all mandatory arguments were supplied
				def_count = len(inspect.getargspec(self.func).defaults)
				mand_count = len(real_args) - def_count
				mand_args = real_args[:mand_count]
				for arg in mand_args:
					if arg not in params:
						return {'status': 400}				
					
				return self.func(**params)

# Controller class called when an HTTP request comes
class Controller (object):
	def __call__(self, env, start_response):
		res = Response (content_type = 'text/plain', status = 200)
		req = Request (env)
		url = req.path_info
		
		additional_params = dict(req.params)
		additional_params['request'] = req
		additional_params['response'] = res
		additional_params['method'] = req.method
		additional_params['headers'] = req.headers
		
		for handler in UrlCallableFunction.request_handlers:
			result = handler.call_if_matches (url, additional_params)
			if result: 
				if isinstance (result, str):
					res.body = result
				elif isinstance (result, dict):
					if 'body' in result: res.body = result['body']
					if 'charset' in result: res.charset = result['charset']
					if 'content_type' in result: res.content_type = result['content_type']
					if 'additional_headers' in result: res.headers.update(result['additional_headers'])
					if 'status' in result: res.status = result['status']
				break
		
		return res (env, start_response)

# Decorator for request handlers
# It just stores all handler functions in a list inside UrlCallableFunction class
def url_pattern (url_pattern, methods = ['GET', 'POST', 'PUT', 'DELETE']):
	def wrap (f):
		UrlCallableFunction.request_handlers.append (UrlCallableFunction (f, url_pattern, methods))
		return f
	return wrap
