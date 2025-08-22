# Use official Python Alpine image as base
FROM python:3.13-alpine

# Set working directory inside the container
WORKDIR /app

# Install build dependencies for compiling Python packages (like pandas, joblib)
RUN apk add --no-cache \
    build-base \
    gfortran \
    musl-dev \
    linux-headers \
    bash \
    git \
    && apk add --no-cache --virtual .build-deps python3-dev py3-pip

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir models

# Copy the rest of the application code
COPY . .

# Run model training (creates models/*.pkl)
RUN python train_models.py

# Expose the port FastAPI will run on
EXPOSE 8000

# Debug: keep the container alive
CMD ["tail", "-f", "/dev/null"]
