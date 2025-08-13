# ======================================
# IMPORTS & SETTINGS
# ======================================
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import seaborn as sns
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn import metrics
import joblib

# ======================================
# LOAD THE NEW DATA
# ======================================
data = pd.read_csv('./kaggle/input/CAR_DETAILS_FROM_CAR_DEKHO.csv')

# Preview the data
print(data.head())
print("Number of Rows:", data.shape[0])
print("Number of Columns:", data.shape[1])
print(data.info())

# ======================================
# FEATURE ENGINEERING
# ======================================
# Create Age from 'year'
current_year = datetime.datetime.now().year
data['age'] = current_year - data['year']
data.drop('year', axis=1, inplace=True)

# Drop the car name (not useful for modeling unless you extract brand)
data.drop('name', axis=1, inplace=True)

# ======================================
# ENCODING CATEGORICAL FEATURES
# ======================================
# Convert string categories into numerical labels
data['fuel'] = data['fuel'].map({'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'LPG': 3, 'Electric': 4})
data['seller_type'] = data['seller_type'].map({'Dealer': 0, 'Individual': 1, 'Trustmark Dealer': 2})
data['transmission'] = data['transmission'].map({'Manual': 0, 'Automatic': 1})
data['owner'] = data['owner'].map({
    'First Owner': 0,
    'Second Owner': 1,
    'Third Owner': 2,
    'Fourth & Above Owner': 3,
    'Test Drive Car': 4
})

# ======================================
# DROP NULLS (if any)
# ======================================
data.dropna(inplace=True)

# ======================================
# DEFINE FEATURES AND TARGET
# ======================================
X = data.drop('selling_price', axis=1)
y = data['selling_price']

# ======================================
# TRAIN / TEST SPLIT
# ======================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ======================================
# MODEL TRAINING
# ======================================
# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
r2_lr = metrics.r2_score(y_test, y_pred_lr)

# Random Forest
rf = RandomForestRegressor()
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
r2_rf = metrics.r2_score(y_test, y_pred_rf)

# XGBoost
xgb = XGBRegressor()
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
r2_xgb = metrics.r2_score(y_test, y_pred_xgb)

# ======================================
# RESULTS COMPARISON
# ======================================
results = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'R2 Score': [r2_lr, r2_rf, r2_xgb]
})
print("\nModel Performance Comparison:\n")
print(results)

# ======================================
# SAVE THE BEST MODEL
# ======================================
# Assuming XGBoost is best
joblib.dump(xgb, './models/car_dekho_model.pkl')
print("\n✅ Best model (XGBoost) saved to ./models/car_dekho_model.pkl")

# ======================================
# SAMPLE PREDICTION
# ======================================
sample = pd.DataFrame({
    'km_driven': [70000],
    'fuel': [0],              # Petrol
    'seller_type': [1],       # Individual
    'transmission': [0],      # Manual
    'owner': [0],             # First Owner
    'age': [2025 - 2007]      # Age = 18
})

model = joblib.load('./models/car_dekho_model.pkl')
prediction = model.predict(sample)
print(f"\n📈 Predicted Price: ৳{prediction[0]:,.2f}")

import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

# Predict using the best model (e.g., XGBoost)
y_pred = xgb.predict(X_test)

# Calculate MAE
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error (MAE): ৳{mae:,.2f}")

# Plot Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', edgecolors='k', alpha=0.6, label='Predicted vs Actual')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2, linestyle='--', label='Ideal Prediction')
plt.title(f'Actual vs Predicted Selling Price\nMAE = ৳{mae:,.2f}')
plt.xlabel('Actual Selling Price')
plt.ylabel('Predicted Selling Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
