# Use official Python image as base
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir models

# Copy the rest of the application code
COPY --chown=root:root . .

# Run model training (creates models/*.pkl)
RUN python train_models.py

# Expose the port FastAPI will run on
EXPOSE 8000

# Debug: keep the container alive 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["tail", "-f", "/dev/null"]
