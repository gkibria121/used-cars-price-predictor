# Use official Python image as base
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir models

# Copy the rest of the application code
COPY . .
RUN python train_models.py
# Expose the port FastAPI will run on
EXPOSE 8000
RUN pwd
# Command to run the FastAPI app with Uvicorn
CMD ["tail", "-f", "/dev/null"]
