from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
# Load your trained model
model = joblib.load('./models/Car_details_v3.pkl')

# Define request body model
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
# Create FastAPI instance
app = FastAPI(title="Car Price Prediction API", version="1.0") 
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
@app.get("/")
def root():
    return {"message": "Car Price Prediction API is running"}

@app.post("/predict")
def predict(features: CarFeatures):
 
    data_new = pd.DataFrame([features.dict()])

    # Make prediction
    prediction = model.predict(data_new)[0]

    return {
        "predicted_price": round(float(prediction), 2),
        "currency": "BDT"
    }
