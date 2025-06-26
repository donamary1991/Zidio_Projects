import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/transactions.csv", parse_dates=["timestamp"])

df = load_data()

# Sidebar
st.sidebar.title("🔍 Filters")
selected_location = st.sidebar.multiselect(
    "Select Locations", df['location'].unique(), default=df['location'].unique()
)

# Filter by location
df_filtered = df[df['location'].isin(selected_location)]

# KPIs
total_tx = len(df_filtered)
fraud_tx = df_filtered['is_fraud'].sum()
legit_tx = total_tx - fraud_tx
fraud_pct = round((fraud_tx / total_tx) * 100, 2)

col1, col2, col3 = st.columns(3)
col1.metric("💳 Total Transactions", total_tx)
col2.metric("🚨 Fraudulent Transactions", fraud_tx)
col3.metric("⚠️ Fraud %", f"{fraud_pct} %")

# Fraud vs Legit Pie Chart
st.subheader("🔢 Fraud vs Legit Distribution")
fig_pie = px.pie(
    df_filtered,
    names='is_fraud',
    title="Fraudulent vs Legit Transactions",
    color_discrete_map={0: "green", 1: "red"},
    labels={0: "Legit", 1: "Fraud"}
)
st.plotly_chart(fig_pie, use_container_width=True)

# Time Series of Transactions
st.subheader("📈 Transaction Amount Over Time")
fig_time = px.line(
    df_filtered.sort_values("timestamp"),
    x="timestamp", y="TransactionAmt", color="is_fraud",
    color_discrete_map={0: "green", 1: "red"},
    title="Transaction Amount Trend"
)
st.plotly_chart(fig_time, use_container_width=True)

# bubblemap by Location


# Location mapping
location_map = {
    'US': (37.0902, -95.7129),
    'IN': (20.5937, 78.9629),
    'CN': (35.8617, 104.1954),
    'BR': (-14.2350, -51.9253)
}

# Map lat/lon from location
df_filtered["lat"] = df_filtered["location"].map(lambda x: location_map.get(x, (0, 0))[0])
df_filtered["lon"] = df_filtered["location"].map(lambda x: location_map.get(x, (0, 0))[1])

# Filter only fraud transactions
fraud_df = df_filtered[df_filtered["is_fraud"] == 1]

# Normalize TransactionAmt for bubble size
scaler = MinMaxScaler()
fraud_df["scaled_amt"] = scaler.fit_transform(fraud_df[["TransactionAmt"]])

# Bubble map
st.subheader("🌍 Fraud Bubble Map by Location")

if not fraud_df.empty:
    fig_bubble = px.scatter_mapbox(
        fraud_df,
        lat="lat", lon="lon",
        size="scaled_amt",
        color="TransactionAmt",
        hover_name="location",
        hover_data={"lat": False, "lon": False, "scaled_amt": False},
        color_continuous_scale="Reds",
        size_max=40,
        zoom=1.5,
        mapbox_style="carto-positron",
        title="Fraud Bubble Map"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
else:
    st.warning("No fraudulent transactions found for the selected locations.")



# Data Table
st.subheader("📄 Transactions Table (Top 1000 rows)")
st.dataframe(df_filtered.head(1000))  # Or any smaller slice like .sample(500)
min_amt = st.sidebar.slider("Min Transaction Amount", float(df_filtered['TransactionAmt'].min()), float(df_filtered['TransactionAmt'].max()), 0.0)
df_filtered = df_filtered[df_filtered['TransactionAmt'] >= min_amt]

st.dataframe(df_filtered.head(500))  # Display after filtering

