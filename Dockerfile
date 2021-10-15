FROM python:3.10

COPY application.py application.py

COPY helper.py helper.py

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV FLASK_APP=application.py

EXPOSE 5000

CMD flask run --host=0.0.0.0
