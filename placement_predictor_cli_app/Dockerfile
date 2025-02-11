# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files to the container
COPY requirements.txt .
COPY cli.py .
COPY models/ models/
COPY X_test.csv .

# Ensure the 'predictions' folder exists
RUN mkdir -p predictions

# Install dependencies with exact versions
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the CLI script
CMD ["python", "cli.py"]
