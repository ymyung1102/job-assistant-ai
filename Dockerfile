# Use official Python image
FROM python:3.11-slim

# Environment variables
ENV PYTHONUNBUFFERED=1


# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpoppler-cpp-dev \
    build-essential \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose the Flask port
EXPOSE 5000

# Set the entrypoint
CMD ["python", "-m", "app.main"]
