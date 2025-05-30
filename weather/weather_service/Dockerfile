FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose port (adjust if needed)
EXPOSE 8011

# Start the app
CMD ["/app/entrypoint.sh"]
