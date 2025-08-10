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
from sklearn import metrics
import joblib

# ======================================
# LOAD THE DATA
# ======================================
data = pd.read_csv('./kaggle/input/car_data.csv')

print(data.head())
print("Number of Rows:", data.shape[0])
print("Number of Columns:", data.shape[1])
data.info()
print("Missing values:\n", data.isnull().sum())
print(data.describe())

# ======================================
# FEATURE ENGINEERING
# ======================================
date_time = datetime.datetime.now()
data['Age'] = date_time.year - data['Year']
data.drop('Year', axis=1, inplace=True)

# ======================================
# OUTLIER REMOVAL
# ======================================
sns.boxplot(data['Selling_Price'])
data = data[~(data['Selling_Price'] >= 33.0) & (data['Selling_Price'] <= 35.0)]

# ======================================
# ENCODING CATEGORICAL VARIABLES
# ======================================
data['Fuel_Type'] = data['Fuel_Type'].map({'Petrol': 0, 'Diesel': 1, 'CNG': 2})
data['Seller_Type'] = data['Seller_Type'].map({'Dealer': 0, 'Individual': 1})
data['Transmission'] = data['Transmission'].map({'Manual': 0, 'Automatic': 1})

# ======================================
# DEFINE FEATURES AND TARGET
# ======================================
X = data.drop(['Car_Name', 'Selling_Price'], axis=1)
y = data['Selling_Price']

# ======================================
# TRAIN / TEST SPLIT
# ======================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# ======================================
# MODEL TRAINING & EVALUATION
# ======================================
lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
r2_score = metrics.r2_score(y_test, y_pred)
print("Linear Regression R2 Score:", r2_score)

# ======================================
# FINAL MODEL SELECTION & SAVING
# ======================================
lr_final = LinearRegression().fit(X, y)
joblib.dump(lr_final, './models/car_price_predictor')

# Load the model back
model = joblib.load('./models/car_price_predictor')

# ======================================
# TEST PREDICTION
# ======================================
data_new = pd.DataFrame({
    'Present_Price': [5.59],
    'Kms_Driven': [27000],
    'Fuel_Type': [0],       # Petrol
    'Seller_Type': [0],     # Dealer
    'Transmission': [0],    # Manual
    'Owner': [0],
    'Age': [8]
})

print("Predicted Selling Price:", model.predict(data_new)) 
