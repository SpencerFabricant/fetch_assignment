FROM python:3.10

RUN mkdir /flask

COPY app.py /flask/app.py
COPY requirements.txt /flask/requirements.txt

WORKDIR /flask
RUN pip3 install -r requirements.txt
cmd [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]

