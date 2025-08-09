# ======================================
# IMPORTS & SETTINGS
# ======================================
import warnings
warnings.filterwarnings('ignore')  # Ignore all warnings for cleaner output

import pandas as pd
import datetime
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn import metrics
import joblib

# ======================================
# LOAD THE DATA
# ======================================
# Read the dataset from the local Kaggle-style folder
data = pd.read_csv('./kaggle/input/car_data.csv')

# Preview the first few rows
print(data.head())

# Show the last few rows (optional)
data.tail()

# Shape of dataset
data.shape
print("Number of Rows", data.shape[0])
print("Number of Columns", data.shape[1])

# Info about data types and nulls
data.info()

# Count missing values in each column
data.isnull().sum()

# Summary statistics for numerical columns
data.describe()

# Preview just the first row
data.head(1)

# ======================================
# FEATURE ENGINEERING
# ======================================
# Calculate the 'Age' of each car from the current year
date_time = datetime.datetime.now()
data['Age'] = date_time.year - data['Year']

# Remove the 'Year' column since it's now redundant
data.drop('Year', axis=1, inplace=True)

# ======================================
# OUTLIER REMOVAL
# ======================================
# Visualize Selling Price distribution to identify outliers
sns.boxplot(data['Selling_Price'])

# Sort Selling Price in descending order to inspect large values
sorted(data['Selling_Price'], reverse=True)

# Remove extreme price outliers between 33 and 35
data = data[~(data['Selling_Price'] >= 33.0) & (data['Selling_Price'] <= 35.0)]

# ======================================
# ENCODING CATEGORICAL VARIABLES
# ======================================
# Map Fuel_Type to numerical values
data['Fuel_Type'] = data['Fuel_Type'].map({'Petrol': 0, 'Diesel': 1, 'CNG': 2})

# Map Seller_Type to numerical values
data['Seller_Type'] = data['Seller_Type'].map({'Dealer': 0, 'Individual': 1})

# Map Transmission to numerical values
data['Transmission'] = data['Transmission'].map({'Manual': 0, 'Automatic': 1})

# ======================================
# DEFINE FEATURES AND TARGET
# ======================================
X = data.drop(['Car_Name', 'Selling_Price'], axis=1)  # Features
y = data['Selling_Price']  # Target variable

# ======================================
# TRAIN / TEST SPLIT
# ======================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# ======================================
# MODEL TRAINING
# ======================================
lr = LinearRegression()
lr.fit(X_train, y_train)

rf = RandomForestRegressor()
rf.fit(X_train, y_train)

xgb = GradientBoostingRegressor()
xgb.fit(X_train, y_train)

xg = XGBRegressor()
xg.fit(X_train, y_train)

# ======================================
# MODEL EVALUATION
# ======================================
y_pred1 = lr.predict(X_test)
y_pred2 = rf.predict(X_test)
y_pred3 = xgb.predict(X_test)
y_pred4 = xg.predict(X_test)

# Calculate R2 scores for each model
score1 = metrics.r2_score(y_test, y_pred1)
score2 = metrics.r2_score(y_test, y_pred2)
score3 = metrics.r2_score(y_test, y_pred3)
score4 = metrics.r2_score(y_test, y_pred4)

print(score1, score2, score3, score4)

# Create DataFrame to compare model performance
final_data = pd.DataFrame({
    'Models': ['LR', 'RF', 'GBR', 'XG'],
    'R2_SCORE': [score1, score2, score3, score4]
})

# ======================================
# FINAL MODEL SELECTION & SAVING
# ======================================
# Retrain XGBRegressor on full dataset
xg_final = XGBRegressor().fit(X, y)

# Save model to 'models' folder
joblib.dump(xg_final, './models/car_price_predictor')

# Load the model back from file
model = joblib.load('./models/car_price_predictor')

# ======================================
# TEST PREDICTION
# ======================================
# Create a sample new car data point
data_new = pd.DataFrame({
    'Present_Price': 5.59,
    'Kms_Driven': 27000,
    'Fuel_Type': 0,       # Petrol
    'Seller_Type': 0,     # Dealer
    'Transmission': 0,    # Manual
    'Owner': 0,
    'Age': 8
}, index=[0])

# Predict price for new car
print(model.predict(data_new))
