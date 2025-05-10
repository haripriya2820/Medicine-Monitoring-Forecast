import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------- [EMAIL FUNCTION] -------------------
def send_email(sender_email, sender_app_password, recipient_email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(sender_email, sender_app_password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# ------------------- [LOAD DATA FUNCTION] -------------------
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['datum'] = pd.to_datetime(df['datum'])
    df.set_index('datum', inplace=True)
    return df

# ------------------- [ARIMA FORECAST FUNCTION] -------------------
def sarima_forecast(df, periods=4, seasonal_order=(0,0,0,52)):
    predictions = {}
    
    for column in df.columns:
        # Using SARIMAX for seasonal ARIMA
        model = SARIMAX(df[column], order=(2,0,0), seasonal_order=seasonal_order,
                        enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=False)
        forecast = model_fit.forecast(steps=periods)
        predictions[column] = forecast
    
    forecast_dates = pd.date_range(start=df.index[-1], periods=periods+1, freq='W')[1:]
    return pd.DataFrame(predictions, index=forecast_dates)
# ------------------- [STREAMLIT UI] -------------------
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", ["📉 Demand Forecasting", "📦 Stock Alerts"])
uploaded_file = st.sidebar.file_uploader("📂 Upload File", type=["csv"])
forecast_weeks = st.sidebar.slider("📅 Select Forecast Period (Weeks)", min_value=2, max_value=8, value=4)

if uploaded_file is not None:
    st.session_state.df = load_data(uploaded_file)
    st.session_state.forecast_df = sarima_forecast(st.session_state.df, periods=forecast_weeks)
    st.sidebar.success("✅ Data Loaded Successfully!")

if "forecast_df" in st.session_state:
    forecast_df = st.session_state.forecast_df
# ------------------- [DEMAND FORECASTING PAGE] -------------------
if page == "📉 Demand Forecasting":
    st.title("📊 Medicine Demand Forecasting")

    if "forecast_df" in st.session_state:
        selected_medicines = st.multiselect("Select Medicines to Forecast", list(forecast_df.columns), default=list(forecast_df.columns)[:3])

        if selected_medicines:
            st.write("### 📈 Forecasted Sales Trends")
            fig = go.Figure()
            for medicine in selected_medicines:
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[medicine], mode='lines+markers', name=medicine))

            fig.update_layout(title="Medicine Sales Forecast", xaxis_title="Weeks", yaxis_title="Predicted Sales", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            st.write("### 📋 Forecast Data Table")
            st.dataframe(forecast_df[selected_medicines].style.format("{:.2f}"))


# ------------------- [STOCK ALERTS PAGE] -------------------
if page == "📦 Stock Alerts":
    st.title("🚨 Medicine Stock Alerts")

    if "forecast_df" in st.session_state:
        selected_medicine = st.selectbox("Select a Medicine", list(forecast_df.columns))

        # User enters stock details
        col1, col2 = st.columns(2)
        with col1:
            initial_stock = st.number_input(f"Enter current stock for {selected_medicine} (Default is 0)", min_value=0, value=0)
        with col2:
            low_stock_threshold = st.number_input(f"⚠️ Set Low Stock Threshold", min_value=10, value=50)

        # Only calculate stock depletion if the user has entered stock
        if initial_stock > 0:
            stock_levels = [initial_stock]
            restock_week = None
            email_sent = False  # Track whether email has been sent

            for week in range(forecast_weeks):
                new_stock = stock_levels[-1] - forecast_df[selected_medicine].iloc[week]

                # Check if stock falls below threshold
                if new_stock < low_stock_threshold and restock_week is None:
                    restock_week = week + 1
                    
                    if not email_sent:  # Ensure only one email is sent
                        sender_email = 'abimedicine01@gmail.com'  # Replace with your email
                        sender_app_password = 'pswj npft bibu jmgq'  # Replace with your Gmail app password
                        recipient_email = 'hemakalyani2005@gmail.com'  # Replace with recipient's email
                        subject = f"⚠️ Low Stock Alert: {selected_medicine}"
                        message = f"Stock for {selected_medicine} is low! Expected depletion by Week {restock_week}. Please restock soon."

                        send_email(sender_email, sender_app_password, recipient_email, subject, message)
                        email_sent = True  # Prevent multiple emails

                stock_levels.append(max(new_stock, 0))

            # Display stock level chart
            st.write("### 📉 Stock Levels Over Time")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(range(forecast_weeks+1)), 
                y=stock_levels, 
                marker_color=['green' if s > low_stock_threshold else 'orange' if s > 0 else 'red' for s in stock_levels]
            ))
            fig.update_layout(title=f"Stock Levels for {selected_medicine}", xaxis_title="Weeks", yaxis_title="Stock Level")
            st.plotly_chart(fig, use_container_width=True)

            # Display stock alert message
            if restock_week:
                st.error(f"⚠️ **Warning!** {selected_medicine} needs restocking by **Week {restock_week}**!")
            else:
                st.success(f"✅ Stock for {selected_medicine} is sufficient for the next {forecast_weeks} weeks!")

        else:
            st.warning("⚠️ Please enter the current stock to check for alerts.")

