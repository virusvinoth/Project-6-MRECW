import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
# 1. Load your sales data
df = pd.read_csv("Train.csv")
# 2. Prepare data for Prophet
df['ds'] = pd.to_datetime(df['order_date']) # Rename date column to 'ds'
df['y'] = df['units_sold'] # Rename sales column to 'y'
df = df[['ds', 'y']] # Keep only required columns
# 3. Initialize and fit the model
model = Prophet()
model.fit(df)
# 4. Forecast for 30 future days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
# 5. Plot the forecast
model.plot(forecast)
plt.title("Sales Forecast")
plt.show()
# 6. Optional: Plot components (trend, weekly pattern)
model.plot_components(forecast)
plt.show()