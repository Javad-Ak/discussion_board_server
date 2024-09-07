# Use an official Python runtime as a parent image
FROM python:3.11-alpine AS django_app

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container to /django_app
WORKDIR /django_app
RUN mkdir -p /django_app/static
RUN mkdir -p /django_app/media

# Copy the current directory files (on your machine) to the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# You can also run "docker-compose exec django_app python manage.py migrate --noinput"
RUN chmod +x ./scripts/entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]