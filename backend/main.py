from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
# Load your trained model
model = joblib.load('./models/car_price_predictor')

# Define request body model
class CarFeatures(BaseModel):
    Present_Price: float
    Kms_Driven: float
    Fuel_Type: float
    Seller_Type: float
    Transmission: float
    Owner: float
    Age: float

# Create FastAPI instance
app = FastAPI(title="Car Price Prediction API", version="1.0")
# Allow origins that will access your API (use ["*"] to allow all)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    # Add your frontend URL(s) here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, OPTIONS, etc)
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Car Price Prediction API is running"}

@app.post("/predict")
def predict(features: CarFeatures):
    # Convert request to DataFrame
    data_new = pd.DataFrame([features.dict()])

    # Make prediction
    prediction = model.predict(data_new)[0]

    return {
        "predicted_price": round(float(prediction), 2),
        "currency": "Lakhs"
    }
