import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from scipy.stats import norm
import matplotlib.pyplot as plt

st.set_page_config(page_title="Inventory Optimization Dashboard", layout="wide")
st.title("📦 Inventory Forecasting & EOQ Optimization Tool")

uploaded_file = st.file_uploader("Upload your retail demand CSV", type=["csv"])

st.markdown("📂 Don't have a CSV? Try our [demo file](https://github.com/CleanBandittt/inventory-forecast-dashboard/blob/main/Mock_Retail_Demand_Data.csv).")


if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = {'date', 'sku_id', 'weekly_demand', 'lead_time_days', 'unit_cost', 'order_cost'}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain the following columns: date, sku_id, weekly_demand, lead_time_days, unit_cost, order_cost")
    else:
        df['date'] = pd.to_datetime(df['date'])
        sku_list = df['sku_id'].unique().tolist()
        sku_choice = st.selectbox("Select SKU", sku_list)
        df_sku = df[df['sku_id'] == sku_choice].copy()

        service_level = st.slider("Select Service Level (Z-Score Basis)", 0.85, 0.999, 0.95, step=0.01)

        def forecast_demand(df_sku):
            df_prophet = df_sku[['date', 'weekly_demand']].rename(columns={'date': 'ds', 'weekly_demand': 'y'})
            model = Prophet(weekly_seasonality=True)
            model.fit(df_prophet)
            future = model.make_future_dataframe(periods=12, freq='W')
            forecast = model.predict(future)
            return forecast, model

        def optimize_inventory(df_sku, service_level):
            avg_demand = df_sku['weekly_demand'].mean()
            std_demand = df_sku['weekly_demand'].std()
            unit_cost = df_sku['unit_cost'].iloc[0]
            order_cost = df_sku['order_cost'].iloc[0]
            lead_time_days = df_sku['lead_time_days'].iloc[0]

            annual_demand = avg_demand * 52
            holding_cost = unit_cost * 0.20
            z = norm.ppf(service_level)

            EOQ = np.sqrt((2 * annual_demand * order_cost) / holding_cost)
            safety_stock = z * std_demand * np.sqrt(lead_time_days / 7)
            ROP = (avg_demand * (lead_time_days / 7)) + safety_stock

            return {
                'SKU': df_sku['sku_id'].iloc[0],
                'EOQ': round(EOQ),
                'ROP': round(ROP),
                'Safety Stock': round(safety_stock),
                'Avg Demand': round(avg_demand, 2),
                'Std Dev': round(std_demand, 2),
                'Lead Time (days)': lead_time_days,
                'Service Level': f"{int(service_level * 100)}%",
                'Unit Cost': round(unit_cost, 2),
                'Order Cost': order_cost
            }

        forecast, model = forecast_demand(df_sku)
        result = optimize_inventory(df_sku, service_level)

        st.subheader("📊 Inventory Optimization Summary")
        st.dataframe(pd.DataFrame([result]))

        st.subheader("📈 Forecasted Weekly Demand")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        with st.expander("📉 Decomposition: Trend + Seasonality"):
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)
