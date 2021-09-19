# Auction commerce Docker image (single-container)
FROM python:3.9

# Copy project (src + requirements)
COPY . /usr/app/src
WORKDIR /usr/app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install all src dependencies
RUN pip install --requirement requirements.txt
