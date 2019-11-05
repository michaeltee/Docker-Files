FROM python:2.7-alpine

MAINTAINER Michael Taylor <michael@michaeltaylor.io>

COPY . /app

WORKDIR /app

RUN pip install requests pyjwt flask

ENV MERCHANT_ID=testrest
ENV HOST=testflex.cybersource.com
ENV REQUEST_TARGET=/flex/v1/keys?format=JWT
ENV ENCRYPTION_TYPE=RsaOaep256
ENV TARGET_ORIGIN=http://localhost:5000
ENV KEY_ID=08c94330-f618-42a3-b09d-e1e43be5efda
ENV SECRET=testsecretkey

CMD ["sh", "-c", "python app.py"]