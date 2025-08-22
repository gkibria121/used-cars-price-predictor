FROM python:3.13-alpine

WORKDIR /app

# Install build tools
RUN apk add --no-cache \
    gcc g++ musl-dev cmake python3-dev libexecinfo-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir models

COPY --chown=root:root . .

RUN python train_models.py

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
