[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
👉 [Launch Dashboard](https://inventory-forecast-dashboard-an3rsr4kgq85cvkypggbih.streamlit.app)

# Inventory Forecast Dashboard 📦📈

A Streamlit-powered web app for demand forecasting and inventory optimization using Prophet and EOQ models.

## 📂 How to Use

1. Upload your CSV file.
2. Select an SKU.
3. Adjust the Service Level using the slider.
4. View forecast, EOQ, ROP, and safety stock calculations.

## 📝 Required CSV Columns

Your file must contain the following **case-sensitive** column names:
- `date` (YYYY-MM-DD format)
- `sku_id`
- `weekly_demand`
- `lead_time_days`
- `unit_cost`
- `order_cost`

## 🛠 Powered By
- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Facebook Prophet](https://facebook.github.io/prophet/)
- NumPy, Pandas, SciPy

---

🔓 Licensed under the MIT License
