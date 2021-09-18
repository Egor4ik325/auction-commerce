# Auction commerce Docker image (single-container)
FROM python:3.9

# Copy project (src + requirements)
COPY . /usr/app/src
WORKDIR /usr/app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install all src dependencies
RUN pip install --requirement requirements.txt

# Start developmnet server (listen on requests from anywhere)
CMD python manage.py runserver 0.0.0.0:8000