🧠 ML-Based Medicine Monitoring System
📘 Description
The ML-Based Medicine Monitoring System is an intelligent forecasting solution that helps healthcare providers, hospitals, and pharmacies manage their medicine inventory efficiently. By leveraging time series analysis , this system predicts the future demand for various medicines and raises early alerts when stock levels are projected to fall below critical thresholds.

This tool is particularly useful for improving medicine availability, reducing stock-outs, and enhancing data-driven decision-making in pharmaceutical logistics.

🚀 Features
✅ Time series forecasting using ARIMA

📉 Historical trend analysis of medicine demand

📦 Intelligent stock alert system based on predicted shortages

📊 Visual representation of demand trends and forecasts

⏱ Scalable and easily adaptable to new datasets

🧾 Dataset Overview
The dataset includes daily records of pharmaceutical consumption. Each column represents a unique medicine category, and the date-wise usage is tracked over time.

Sample Columns:
datum: Date of entry 

M01AB, M01AE, N02BA, N02BE, ...: Medicine codes indicating various drug categories

🛠️ Technologies Used
Python 3.x

Pandas, NumPy – Data processing

Matplotlib, Seaborn – Visualization

Statsmodels – SARIMA time series modeling

(Optional) Streamlit / Flask – Web interface

🧪 How It Works
Data Preprocessing

Format dates, clean null values, and filter medicine columns.

Modeling with ARIMA

Fit individual ARIMA models for each medicine code.

Forecast Generation

Predict future demand for a configurable time window (e.g., next 30 days).

Stock Alerting

Compare predicted demand with available stock thresholds to trigger alerts and notify with email
