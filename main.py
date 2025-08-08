from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from prophet import Prophet
import io
app = FastAPI()

@app.post("/forecast/")
async def forecast_sales(file: UploadFile = File(...)):
    try:
# Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    # Validate necessary columns
        if 'order_date' not in df.columns or 'units_sold' not in df.columns:
            return JSONResponse(status_code=400, content={"error": "CSV must have 'order_date' and 'units_sold' columns"})
# Prepare Data
        df['ds'] = pd.to_datetime(df['order_date'])
        df['y'] = df['units_sold']
        df = df[['ds', 'y']]
        # Train Prophet model
        model = Prophet()
        model.fit(df)
        # Forecast for 30 future days
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        # Return only required forecast columns as JSON
        forecast_result = forecast[['ds', 'yhat', 'yhat_lower','yhat_upper']].tail(30)
        result = forecast_result.to_dict(orient='records')
        return {"forecast": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})