# restGET v. 1.1
# Michael Taylor, March 2019.

import requests
import cybersource
import json 
import os
from sys import exit, argv

(script, show_progress) = argv

if show_progress == "false":
   cybs = cybersource.rest()
   signed_headers = cybs.build_get_signature("/reporting/v3/report-downloads?" + \
                  "organizationId=" + os.environ['MERCHANT_ID'] + \
                  "&reportDate=" + os.environ['REPORT_DATE'] + \
                  "&reportName=" + os.environ['REPORT_NAME'])
   r = requests.get("https://" + os.environ['HOST'] + \
               ".cybersource.com/reporting/v3/report-downloads?" + \
               "organizationId=" + os.environ['MERCHANT_ID'] + \
               "&reportDate=" + os.environ['REPORT_DATE'] + \
               "&reportName=" + os.environ['REPORT_NAME'], 
               headers=signed_headers)

   filename = os.environ['MERCHANT_ID']+'.'+os.environ['REPORT_NAME']+'.'+os.environ['REPORT_DATE']+'.'+os.environ['FILE_FORMAT']
   if r.status_code == 200:
      print "HTTP 200 received, writing %s in mounted volume...." % filename
      with open('/reports/%s' % filename, mode='wb') as localfile:
         localfile.write(r.content)
   else:
      exit("Unsuccessful request, no report written.")

elif show_progress == "true":
   print "\n[restGet.py] - Instantiating cybersource.rest_verbose()..."
   cybs = cybersource.rest_verbose()
   print "\n[restGet.py] - Start signature generation..."
   signed_headers = cybs.build_get_signature("/reporting/v3/report-downloads?" + \
                  "organizationId=" + os.environ['MERCHANT_ID'] + \
                  "&reportDate=" + os.environ['REPORT_DATE'] + \
                  "&reportName=" + os.environ['REPORT_NAME'])

   print "\n[restGet.py] - Signature generation complete."
   print "\n[restGet.py] - Preparing request..."

   r = requests.get("https://" + os.environ['HOST'] + \
               ".cybersource.com/reporting/v3/report-downloads?" + \
               "organizationId=" + os.environ['MERCHANT_ID'] + \
               "&reportDate=" + os.environ['REPORT_DATE'] + \
               "&reportName=" + os.environ['REPORT_NAME'], 
               headers=signed_headers)

   print "\n[restGet.py] - HTTP GET request initiatied, destination: %s" % r.url
   print "\n[restGet.py] - Request headers: "
   for k,v in r.request.headers.iteritems():
      print "%s = %s" % (k, v)

   print "\n[restGet.py] - HTTP status code: %d" % r.status_code
   print "\n[restGet.py] - Response body: %s" % r.text

   filename = os.environ['MERCHANT_ID']+'.'+os.environ['REPORT_NAME']+'.'+os.environ['REPORT_DATE']+'.'+os.environ['FILE_FORMAT']
   print "\n[restGet.py] - Reply filename: %s" % filename
   if r.status_code == 200:
      print "\n[restGet.py] - Writing %s in mounted volume...." % filename
      with open('/reports/%s' % filename, mode='wb') as localfile:
         localfile.write(r.content)
      print "\n[restGet.py] - Report written to disk successfullly."
   else:
      exit("\n[restGet.py] - Unsuccessful request, no report written.")
