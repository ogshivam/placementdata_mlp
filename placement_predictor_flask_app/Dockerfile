# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files to the container
COPY requirements.txt .
COPY app.py .
COPY models/ models/
COPY testdata.csv .

# Create necessary directories
RUN mkdir -p predictions uploads templates

# Install dependencies with exact versions
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5002

# Set environment variable to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the command to run the Flask app
CMD ["python", "app.py"]