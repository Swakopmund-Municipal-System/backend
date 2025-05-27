FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create database and seed data
RUN python scripts/seed_data.py

# Expose port
EXPOSE 8585

# Use the simple server which works reliably
CMD ["python", "scripts/simple_server.py"] 