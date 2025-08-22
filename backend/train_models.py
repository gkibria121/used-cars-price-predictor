# ======================================
# train_models.py — FIXED (no 'squared' arg; adds RMSE, coeffs, visuals, torque normalization)
# ======================================

import warnings
warnings.filterwarnings('ignore')

import os
import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib


# ======================================
# HELPERS: parsing & normalization
# ======================================
KGFM_TO_NM = 9.80665  # 1 kgf·m ≈ 9.80665 N·m

def extract_float(text):
    """Extract the first floating number from a string; returns np.nan if not found."""
    if pd.isna(text):
        return np.nan
    m = re.search(r'([\d]+(?:\.\d+)?)', str(text))
    return float(m.group(1)) if m else np.nan

def parse_torque_to_nm(tq):
    """
    Parse torque strings like:
    - '190Nm@ 2000rpm'
    - '22.4 kgm at 1750-2750rpm'
    - '12.7@ 2,700(kgm@ rpm)'
    Normalize to N·m.
    """
    if pd.isna(tq):
        return np.nan
    s = str(tq).lower().replace(',', '')
    # Capture a value and its nearby unit if present
    m = re.search(r'([\d]+(?:\.\d+)?)\s*(nm|n\-?m|kgm|kgf\.?m|kgf\-?m)?', s)
    if not m:
        return np.nan
    value = float(m.group(1))
    unit = m.group(2) or ""
    if 'kg' in unit:  # kgm / kgf·m
        return value * KGFM_TO_NM
    # Assume Nm if unit missing/ambiguous
    return value

def safe_int(x):
    try:
        return int(float(x))
    except Exception:
        return np.nan


# ======================================
# LOAD THE DATA
# ======================================
# Adjust this path if your CSV is elsewhere
data = pd.read_csv('./kaggle/input/Car_details_v3.csv')

print(data.head())
print("Number of Rows:", data.shape[0])
print("Number of Columns:", data.shape[1])
print(data.info())

# ======================================
# FEATURE ENGINEERING
# ======================================
current_year = datetime.datetime.now().year
data['age'] = current_year - data['year']
data.drop('year', axis=1, inplace=True)

# Drop text identifier
data.drop('name', axis=1, inplace=True)

# Clean numeric-from-text columns
data['mileage']   = data['mileage'].apply(extract_float)
data['engine']    = data['engine'].apply(extract_float)
data['max_power'] = data['max_power'].apply(extract_float)
data['torque']    = data['torque'].apply(parse_torque_to_nm)

# Seats may be float in raw; cast to int when safe
data['seats'] = data['seats'].apply(safe_int)

# ======================================
# ENCODING CATEGORICAL FEATURES
# ======================================
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
data = data.dropna().reset_index(drop=True)

# ======================================
# DEFINE FEATURES AND TARGET
# ======================================
TARGET = 'selling_price'
X = data.drop(TARGET, axis=1)
y = data[TARGET]

feature_names = X.columns.tolist()

# ======================================
# TRAIN / TEST SPLIT
# ======================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================================
# TRAIN MODELS
# ======================================
lr = LinearRegression()
rf = RandomForestRegressor(random_state=42)
xgb = XGBRegressor(
    random_state=42,
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9
)

models = {
    'Linear Regression': lr,
    'Random Forest': rf,
    'XGBoost': xgb
}

metrics_rows = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    # FIX: compute RMSE compatibly for older sklearn (no 'squared' kwarg)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    metrics_rows.append([name, r2, mae, rmse])

results = pd.DataFrame(metrics_rows, columns=['Model', 'R2', 'MAE', 'RMSE'])
print("\nModel Performance (Test):\n")
print(results.sort_values('R2', ascending=False))

# ======================================
# SAVE THE BEST MODEL
# ======================================
best_row = results.sort_values('R2', ascending=False).iloc[0]
best_name = best_row['Model']
best_model = models[best_name]

os.makedirs('./models', exist_ok=True)
joblib.dump(best_model, './models/car_details_v3.pkl')
print(f"\n✅ Best model: {best_name} saved to ./models/car_details_v3.pkl (R2 = {best_row['R2']:.4f})")

# ======================================
# LINEAR COEFFICIENTS TABLE
# ======================================
try:
    lr_coefs = pd.DataFrame({
        'feature': feature_names,
        'coefficient': lr.coef_
    }).sort_values('coefficient', key=np.abs, ascending=False)
    print("\nLinear Regression Coefficients (sorted by |coef|):\n")
    print(lr_coefs.head(20))
except Exception as e:
    print("\n[WARN] Could not compute LR coefficients:", e)

# ======================================
# SAMPLE PREDICTION
# ======================================
sample = pd.DataFrame({
    'km_driven': [70000],
    'fuel': [0],              # Petrol
    'seller_type': [1],       # Individual
    'transmission': [0],      # Manual
    'owner': [0],             # First Owner
    'mileage': [20.0],
    'engine': [1197],
    'max_power': [82],
    'torque': [113],          # already in N·m
    'seats': [5],
    'age': [current_year - 2015]
})
loaded = joblib.load('./models/car_details_v3.pkl')
pred = loaded.predict(sample)
print(f"\n📈 Predicted Price (sample): ৳{pred[0]:,.2f}")

# ======================================
# VISUALS
# ======================================

# 1) Actual vs Predicted (best model)
y_pred_best = best_model.predict(X_test)
mae_best  = mean_absolute_error(y_test, y_pred_best)
rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_best, edgecolors='k', alpha=0.6, label='Predicted vs Actual')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
         linewidth=2, linestyle='--', label='Ideal Prediction')
plt.title(f'Actual vs Predicted Selling Price ({best_name})\nMAE = ৳ {mae_best:,.2f} | RMSE = ৳ {rmse_best:,.2f}')
plt.xlabel('Actual Selling Price')
plt.ylabel('Predicted Selling Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2) Univariate regression line: km_driven vs selling_price (illustrative only)
subset = data.sample(n=min(2000, len(data)), random_state=42)
x_uni = subset[['km_driven']]
y_uni = subset['selling_price']
lr_uni = LinearRegression().fit(x_uni, y_uni)
y_uni_pred = lr_uni.predict(x_uni)

# Sort for clean line
order = np.argsort(x_uni.values.ravel())
plt.figure(figsize=(8, 6))
plt.scatter(x_uni, y_uni, s=10, alpha=0.5, edgecolors='none', label='Data')
plt.plot(x_uni.values.ravel()[order], y_uni_pred[order], linewidth=2, label='Regression Line')
plt.title('Univariate Regression: km_driven vs selling_price (illustrative)')
plt.xlabel('km_driven')
plt.ylabel('selling_price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 3) Feature Importance (for tree models)
if hasattr(best_model, 'feature_importances_'):
    importances = pd.Series(best_model.feature_importances_, index=feature_names).sort_values(ascending=False)[:20]
    plt.figure(figsize=(8, 6))
    importances.iloc[::-1].plot(kind='barh')
    plt.title(f'Feature Importance (Top 20) — {best_name}')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()
else:
    print("\n[INFO] Best model has no feature_importances_; skipping importance plot.")
