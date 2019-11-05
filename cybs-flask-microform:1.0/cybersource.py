# CYBS Flex Microform helper library.
# Not officially endorsed, supported, or provided by CyberSource.
# Use at your own risk.

import requests
from datetime import datetime
import base64
import json
import hashlib
import hmac
from collections import OrderedDict
import os

class Flex():
  def __init__(self):
    self.mid = os.environ['MERCHANT_ID']
    #self.credentials = self.get_credentials(mid)
    self.secret = os.environ['SECRET']
    self.key_id = os.environ['KEY_ID']
    self.host = os.environ['HOST']
    self.request_target = os.environ['REQUEST_TARGET']
    self.encryption_type = os.environ['ENCRYPTION_TYPE']
    self.target_origin = os.environ['TARGET_ORIGIN']
    self.body = '{\n  "encryptionType": "%s",\n  "targetOrigin": "%s"\n}' % (self.encryption_type, self.target_origin)

  def build_timestamp(self):
    # CYBS requires a specific timestamp format be used.
    self.date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    return self.date

  def build_signature(self):
    self.digest = "SHA-256=%s" % base64.b64encode(hashlib.sha256(self.body).digest())
    # Build headers in a predictable order.
    self.signed_headers = OrderedDict()
    self.signed_headers['host'] = self.host
    self.signed_headers['date'] = self.build_timestamp()
    self.signed_headers['(request-target)'] = "post " + self.request_target
    self.signed_headers['digest'] = self.digest
    self.signed_headers['v-c-merchant-id'] = self.mid
    self.signed_headers['content-type'] = 'application/json'

    # Next, build signature string with format "k: v\n" for HMAC digestion.
    self.signature_string = str()
    for k, v in self.signed_headers.iteritems():
      self.signature_string+= "\n%s: %s" % (k, v)

    # Trim leading newline char.
    self.signature_string = self.signature_string[1:]

    # Create an HMAC from shared secret and header string.
    self.hash_string = hmac.new(base64.b64decode(self.secret), 
                        self.signature_string, hashlib.sha256).digest()

    # Prepare string of signed headers to add to signature.
    self.headers_string = str()
    for k, v in self.signed_headers.iteritems():
      self.headers_string+= " %s" % k

    # Trim leading newline char.
    self.headers_string = self.headers_string[1:]

    # Construct final signature string that is appended to signed headers.
    self.final_signature = str()
    self.final_signature += 'keyid="%s", ' % self.key_id
    self.final_signature += 'algorithm="HmacSHA256", '
    # Inject list of headers we signed.
    self.final_signature += 'headers="%s", ' % self.headers_string
    # Inject the B64-encoded HMAC signature.
    self.final_signature += 'signature="%s"' % base64.b64encode(self.hash_string)
    # Button it up and add it as a header itself.
    self.signed_headers['signature'] = self.final_signature

    # Not needed for actual request, so we can delete it.
    del self.signed_headers['(request-target)']

    return self.signed_headers
