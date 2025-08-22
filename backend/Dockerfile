# Use official Ubuntu as base
FROM ubuntu:24.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.13 python3-pip python3-venv \
    build-essential cmake git wget curl \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir models

# Copy app source code
COPY  . .

# Run model training
RUN python3 train_models.py

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
