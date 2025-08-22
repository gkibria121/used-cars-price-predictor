from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Car Price Prediction API", version="1.0")

# allow frontend origins
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://used-cars-price-predictor.gkibria121.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    model_path = "./models/car_details_v3.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        raise FileNotFoundError(f"Model file not found: {model_path}")

class CarFeatures(BaseModel):
    km_driven: float
    fuel: float
    seller_type: float
    transmission: float
    owner: float
    mileage: float
    engine: float
    max_power: float
    torque: float
    seats: float
    age: float

@app.get("/")
def root():
    return {"message": "Car Price Prediction API is running"}

@app.post("/predict")
def predict(features: CarFeatures):
    if model is None:
        return {"error": "Model not loaded"}
    data_new = pd.DataFrame([features.dict()])
    prediction = model.predict(data_new)[0]
    return {
        "predicted_price": round(float(prediction), 2),
        "currency": "BDT"
    }
