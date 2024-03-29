FROM python:3.11.5-slim

MAINTAINER "Your name" <email@example.com>
ENV container docker

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY lib/config.py .
COPY src/exchange_rate_update.py .
COPY src/app.py .

CMD ["python", "./app.py"]