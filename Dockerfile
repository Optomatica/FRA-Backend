FROM python:3.10-slim
WORKDIR /app

# Install all system dependencies in one layer
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy data folder
COPY data/ /app/data/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8002
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8002

# Create a startup script that runs migrations then starts the app
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running Alembic migrations..."\n\
alembic upgrade head\n\
echo "Starting application..."\n\
exec python -m uvicorn app:app --host 0.0.0.0 --port 8002' > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Start the application with migrations
CMD ["/app/start.sh"]
