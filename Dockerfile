FROM python:3.11.7

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /usr/src/app/src/

EXPOSE 8000

ENV PYTHONPATH=/usr/src/app/src