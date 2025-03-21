FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and example env file
COPY telegram_scheduler.py .
COPY .env.example .env.example

# Create volume for the .env file and session file
VOLUME ["/app/data"]

# Set the entrypoint
CMD ["python", "telegram_scheduler.py"] 