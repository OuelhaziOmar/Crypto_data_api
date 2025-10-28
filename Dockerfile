# Use official Python 3.12 image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install OS deps for PostgreSQL client and TimescaleDB
RUN apt-get update && apt-get install -y \
    gcc \
    git\
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install git+https://github.com/jmitchel3/timescaledb-python.git
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Set environment variable for FastAPI (optional)
ENV PYTHONUNBUFFERED=1

# Expose port if running FastAPI
EXPOSE 8000

# Command: start FastAPI app
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
