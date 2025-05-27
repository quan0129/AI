# Stock Price Forecasting - 1 Year Data (Extended Model)

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import ta

# 1. Load data (assumes file is named 'stock_data.csv')
df = pd.read_csv("crawl_data/stock_data.csv")

# 2. Convert tradingDate to datetime and sort
df['tradingDate'] = pd.to_datetime(df['tradingDate'])
df = df.sort_values('tradingDate')

# 3. Create time-based features
df['dayofweek'] = df['tradingDate'].dt.dayofweek
df['month'] = df['tradingDate'].dt.month

# 4. Create lag features and technical indicators
df['last_shift_1'] = df['last'].shift(1)
df['last_shift_2'] = df['last'].shift(2)
df['last_shift_5'] = df['last'].shift(5)
df['ma5'] = df['last'].rolling(5).mean()
df['ma10'] = df['last'].rolling(10).mean()
df['rsi'] = ta.momentum.RSIIndicator(close=df['last'], window=14).rsi()

# 5. Create target: next day's closing price
df['target'] = df['last'].shift(-1)

# 6. Drop rows with NaN
df = df.dropna()

# 7. Select features and target
features = [
    'open', 'high', 'low', 'accumulatedVol', 'accumulatedVal', 'lastVol',
    'dayofweek', 'month',
    'last_shift_1', 'last_shift_2', 'last_shift_5',
    'ma5', 'ma10', 'rsi'
]
target = 'target'

X = df[features]
y = df[target]

# 8. Time-based train-test split
train_size = int(len(df) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 9. Train model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 10. Predict and evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE (next-day prediction): {rmse:.4f}")

# 11. Plot results
plt.figure(figsize=(12,6))
plt.plot(y_test.values, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.title("Actual vs Predicted Closing Price - 1 Year Data")
plt.xlabel("Test Sample Index")
plt.ylabel("Price")
plt.grid(True)
plt.show()

# 12. Predict next day's price from latest row
latest_features = df[features].iloc[[-1]]
next_day_prediction = model.predict(latest_features)[0]
print(f"\n Dự đoán giá ngày tiếp theo: {next_day_prediction:.2f}")
