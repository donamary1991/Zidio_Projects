## 📈 Time Series Forecasting for Stock Prices

This project focuses on analyzing and forecasting stock market prices using a variety of statistical and deep learning models, including **ARIMA**, **SARIMA**, **Facebook Prophet**, and **LSTM**. The goal is to evaluate model performance, visualize trends, and accurately predict future stock prices.

## 📊 Dataset

- **Stock:** stockdata.csv
- **Duration:** 2006 to 2017
- **Features:** `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Name`

---

## 🛠️ Technologies Used

- **Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**
- **Statsmodels** for ARIMA/SARIMA
- **Facebook Prophet** for trend + seasonality
- **TensorFlow/Keras** for LSTM model
- **Scikit-learn** for metrics and preprocessing

---

## 🔍 Models Implemented

### 1️⃣ ARIMA (AutoRegressive Integrated Moving Average)
- Forecasts based on autocorrelation and past errors.
- RMSE: ~14.71, R²: -0.42

### 2️⃣ SARIMA (Seasonal ARIMA)
- Enhances ARIMA by modeling seasonal components.
- RMSE: ~13.25, R²: -0.15

### 3️⃣ Facebook Prophet
- Additive model with automatic trend, seasonality, and holidays detection.
- RMSE: ~13.19, R²: -0.14

### 4️⃣ LSTM (Long Short-Term Memory)
- Deep learning RNN-based model for sequential forecasting.
- **RMSE: 1.54**, **R² Score: 0.98** – Highest accuracy!

---

## 📈 Visualizations

- Time series decomposition: Trend, Seasonality, Residual
- Actual vs Forecast plots
- Model training loss curves (for LSTM)
- Outlier detection (Boxplots, scatterplots)

---

## ✅ Results Summary

| Model   | RMSE  | R² Score |
|---------|-------|----------|
| ARIMA   | 14.71 | -0.42    |
| SARIMA  | 13.25 | -0.15    |
| Prophet | 13.19 | -0.14    |
| LSTM    | **1.54** | **0.98**  |

---





