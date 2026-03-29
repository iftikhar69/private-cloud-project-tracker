FROM python:3.12-slim

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest
COPY . .

# Create directory for SQLite DB persistence
RUN mkdir -p /data && chmod 777 /data

EXPOSE 5000

# Volume for persistent database
VOLUME ["/data"]

CMD ["python", "app.py"]