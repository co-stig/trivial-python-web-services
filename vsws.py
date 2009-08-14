#! /usr/bin/env python

from webob import Request, Response
import re
import inspect

# Limitations: 
# Handlers should be static
# Several request parameters with the same name are not supported (only one will be used)

# Defaults:
# Content-Type: text/plain
# 200 OK

# Special arguments:
# request: WebOb Request
# response: WebOb Response
# method: method (GET / POST / PUT / DELETE)

class UrlCallableFunction (object):
	
	param_re = re.compile(r'\$\{(.+?)\}')
	request_handlers = []
	
	def __init__ (self, func, pattern):
		self.pattern = pattern
		self.func = func
		self.param_names = UrlCallableFunction.param_re.findall(pattern)
		self.re = '^' + UrlCallableFunction.param_re.sub('([^/]+?)', pattern) + '$'
		self.re_compiled = re.compile(self.re)
		
	def call_if_matches (self, url, additional_params):
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
				
			return self.func(**params)

# Controller class called when an HTTP request comes
class Controller (object):
	def __call__(self, env, start_response):
		res = Response (content_type = 'text/plain')
		req = Request (env)
		url = req.path_info
		
		additional_params = dict(req.params)
		additional_params['request'] = req
		additional_params['response'] = res
		additional_params['method'] = req.method
		
		for handler in UrlCallableFunction.request_handlers:
			result_text = handler.call_if_matches (url, additional_params)
			if result_text: 
				res.body = result_text
				break
		
		return res (env, start_response)

# Decorator for request handlers
# It just stores all handler functions in a list inside UrlCallableFunction class
def url_pattern (url_pattern):
	def wrap (f):
		UrlCallableFunction.request_handlers.append (UrlCallableFunction (f, url_pattern))
		return f
	return wrap
