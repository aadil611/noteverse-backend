FROM python:3.11.4-slim-buster

# Set the working directory
WORKDIR /usr/src/noteverse

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat
# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/noteverse/entrypoint.sh
RUN chmod +x /usr/src/noteverse/entrypoint.sh

# Copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/noteverse/entrypoint.sh"]