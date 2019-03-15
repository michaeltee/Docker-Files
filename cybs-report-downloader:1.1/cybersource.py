# Dockerized CYBS REST API auth library.  Uses HTTP Signature method.
# Michael Taylor, March 2019.
# V 1.0

import requests
from datetime import datetime
from base64 import b64encode, b64decode
import json
import hashlib
import hmac
from collections import OrderedDict
import os

class rest():
	def __init__(self):
		self.mid = os.environ['MERCHANT_ID']
		# TODO: host validation
		if os.environ['HOST'] == 'apitest':
			self.host = 'apitest'
		elif os.environ['HOST'] == 'api':
			self.host = 'api'
		else:
			quit('ENV error: Illegal host provided, check your runtime variables.')
		self.secret = os.environ['SECRET']
		self.key_id = os.environ['KEY_ID']

	def build_timestamp(self):
		self.date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
		return self.date

	def build_get_signature(self, request_target):
		# Need different GET and POST signature methods due to digest for POST
		self.signed_headers = OrderedDict()
		self.signed_headers['host'] = self.host
		self.signed_headers['date'] = self.build_timestamp()
		self.signed_headers['(request-target)'] = 'get ' + request_target
		self.signed_headers['v-c-merchant-id'] = self.mid

		self.signature_string = str()
		for k, v in self.signed_headers.iteritems():
			self.signature_string+= "\n%s: %s" % (k, v)
		self.signature_string = self.signature_string[1:]

		self.headers_string = str()
		for k, v in self.signed_headers.iteritems():
			self.headers_string+= " %s" % k
		self.headers_string = self.headers_string[1:]

		self.hash_string = hmac.new(b64decode(self.secret), self.signature_string, hashlib.sha256).digest()

		self.final_signature = str()
		self.final_signature += 'keyid="%s", ' % self.key_id
		self.final_signature += 'algorithm="HmacSHA256", '
		self.final_signature += 'headers="%s", ' % self.headers_string
		self.final_signature += 'signature="%s"' % b64encode(self.hash_string)

		self.signed_headers['signature'] = self.final_signature

		del self.signed_headers['(request-target)']

		return self.signed_headers

class rest_verbose():
	def __init__(self):
		self.mid = os.environ['MERCHANT_ID']
		# TODO: host validation
		if os.environ['HOST'] == 'apitest':
			self.host = 'apitest'
		elif os.environ['HOST'] == 'api':
			self.host = 'api'
		else:
			quit('\n[cybersource.py] - ENV error: Illegal host provided, check your runtime variables.')
		self.secret = os.environ['SECRET']
		self.key_id = os.environ['KEY_ID']

	def build_timestamp(self):
		self.date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
		return self.date

	def build_get_signature(self, request_target):
		# Need different GET and POST signature methods due to digest for POST
		self.signed_headers = OrderedDict()
		self.signed_headers['host'] = self.host
		self.signed_headers['date'] = self.build_timestamp()
		self.signed_headers['(request-target)'] = 'get ' + request_target
		self.signed_headers['v-c-merchant-id'] = self.mid

		print "\n[cybersource.py] - Headers to be signed: %s" % self.signed_headers

		self.signature_string = str()
		for k, v in self.signed_headers.iteritems():
			self.signature_string+= "\n%s: %s" % (k, v)
		self.signature_string = self.signature_string[1:]

		print "\n[cybersource.py] - Signature string " + \
				"prior to hashing: \n%s" % self.signature_string

		self.headers_string = str()
		for k, v in self.signed_headers.iteritems():
			self.headers_string+= " %s" % k
		self.headers_string = self.headers_string[1:]

		print "\n[cybersource.py] - Space-separated list of headers " + \
				"to add to signature: %s" % self.headers_string

		self.hash_string = hmac.new(b64decode(self.secret), self.signature_string, hashlib.sha256).digest()

		self.final_signature = str()
		self.final_signature += 'keyid="%s", ' % self.key_id
		self.final_signature += 'algorithm="HmacSHA256", '
		self.final_signature += 'headers="%s", ' % self.headers_string
		self.final_signature += 'signature="%s"' % b64encode(self.hash_string)

		self.signed_headers['signature'] = self.final_signature

		print "\n[cybersource.py] - Final signature: %s" % self.final_signature

		del self.signed_headers['(request-target)']
		print "\n[cybersource.py] - Dropping (request-target) from headers..."

		return self.signed_headers