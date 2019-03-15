FROM python:2.7-alpine

MAINTAINER Michael Taylor <michael@michaeltaylor.io>

COPY . /app

WORKDIR /app

RUN pip install requests

RUN mkdir /reports

ENV MERCHANT_ID=testrest
ENV HOST=apitest
ENV KEY_ID=08c94330-f618-42a3-b09d-e1e43be5efda
ENV SECRET=testsecretkey
ENV REPORT_NAME=test_report_name
ENV REPORT_DATE=2019-01-01
ENV FILE_FORMAT=csv
ENV SHOW_PROGRESS=false

VOLUME /reports

CMD ["sh", "-c", "python restGET.py ${SHOW_PROGRESS}"]
