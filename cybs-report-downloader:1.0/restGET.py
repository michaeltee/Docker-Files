# restGET v. 1.0.
# Michael Taylor, March 2019.

import requests
import cybersource
import json 
import os
from sys import exit

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
