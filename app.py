import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
st.title("📈 Sales Forecast using Prophet")
# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Display raw data
    st.subheader("Raw Data")
    st.write(df.head())
    # Convert and rename
    df['ds'] = pd.to_datetime(df['order_date'])
    df['y'] = df['units_sold']
    df = df[['ds', 'y']]
    # Model training
    model = Prophet()
    model.fit(df)
    # Forecast future
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    # Plot
    st.subheader("Forecast")
    fig1 = model.plot(forecast)
    st.pyplot(fig1)
    # Components
    st.subheader("Forecast Components")
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)
else:
    st.info("Please upload a CSV file with `order_date` and `units_sold`columns.")
