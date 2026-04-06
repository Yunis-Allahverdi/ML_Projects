import pandas as pd
import joblib
import warnings

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

# Load data
df = pd.read_excel('house_dataset.xlsx')

# Cleaning
df['repair'].replace(r'^\s*$', 'yoxdur', regex=True, inplace=True)
df['repair'].fillna('yoxdur', inplace=True)

df.replace({'repair': {'var': 1, 'yoxdur': 0}}, inplace=True)
df.replace({'title_deed': {'var': 1, 'yoxdur': 0}}, inplace=True)
df.replace({'category': {'yeni': 1, 'kohne': 0}}, inplace=True)

df['title_deed'] = df['title_deed'].astype(int)
df['repair'] = df['repair'].astype(int)

df['area'] = (
    df['area']
    .str.replace('m²', '', regex=False)
    .str.replace(' ', '')
    .str.split('.')
    .str[0]
    .astype(int)
)

df['price'] = df['price'].str.replace(' ', '').astype(int)
df['room_number'] = df['room_number'].astype(int)

df.drop(columns=['currency', 'title', 'address', 'region'], inplace=True)
df.drop('price_1m2', axis=1, inplace=True)

df = df[~df['region_new'].isin(['Pirallahi', 'Qaradag'])]

# One-hot encoding
df = pd.get_dummies(df, columns=['region_new'], prefix='region').astype(int)

# Features and target
X = df.drop(columns=['price'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f} AZN")
print(f"R-squared Score: {r2:.4f}")

# Save model and columns
joblib.dump(model, 'model.pkl')
joblib.dump(X.columns.tolist(), 'columns.pkl')

print("Model and columns saved successfully.")