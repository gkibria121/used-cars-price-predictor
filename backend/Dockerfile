FROM python:3.13-alpine

WORKDIR /app

# Install build tools and dependencies
RUN apk add --no-cache gcc g++ musl-dev libffi-dev python3-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir models

COPY  . .

RUN python train_models.py

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
