# Online Retail Prediction System

A full-stack machine learning application that predicts customer revenue and segments using the **UCI Online Retail Dataset**.

---

## 🏗️ Project Structure

```
online_retail_project/
├── backend/
│   ├── app.py              ← Flask REST API (8 endpoints)
│   ├── data_processor.py   ← Data cleaning & feature engineering
│   └── ml_model.py         ← Model training & prediction
├── frontend/
│   └── streamlit_app.py    ← Interactive Streamlit dashboard
├── data/
│   └── Online Retail.xlsx  ← UCI dataset (auto-downloaded)
├── models/
│   ├── revenue_model.pkl   ← Trained Random Forest
│   ├── revenue_scaler.pkl
│   ├── segment_model.pkl   ← Trained Gradient Boosting
│   ├── segment_scaler.pkl
│   └── segment_encoder.pkl
├── train_models.py         ← One-shot training script
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download data & train models
```bash
python train_models.py
```
This will:
- Download the UCI Online Retail dataset (~22MB)
- Clean and engineer RFM features
- Train and save the Revenue Prediction and Segmentation models

### 3. Start the Flask API
```bash
python backend/app.py
# API runs at http://localhost:5000
```

### 4. Start the Streamlit frontend (new terminal)
```bash
streamlit run frontend/streamlit_app.py
# Opens at http://localhost:8501
```

---

## 🤖 ML Models

| Model | Algorithm | Task | Metric |
|-------|-----------|------|--------|
| Revenue Predictor | Random Forest Regressor | Predict customer lifetime value | R², MAE, RMSE |
| Customer Segmenter | Gradient Boosting Classifier | Classify: High/Medium/Low Value | Accuracy |

### Input Features (RFM)
| Feature | Description |
|---------|-------------|
| Recency | Days since last order |
| Frequency | Number of unique orders |
| Avg Order Value | Mean spend per order |
| Total Items | Total quantity purchased |
| Unique Products | Distinct products bought |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/summary` | Dataset KPIs |
| GET | `/api/monthly-revenue` | Time series revenue |
| GET | `/api/top-products?n=10` | Top products |
| GET | `/api/country-stats` | Revenue by country |
| GET | `/api/customer-features` | RFM table |
| POST | `/api/predict/revenue` | Predict revenue |
| POST | `/api/predict/segment` | Predict segment |
| GET | `/api/feature-importance` | Model feature weights |
| POST | `/api/train` | Retrain models |

---

## 📊 Dataset

- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Records:** ~541,909 transactions
- **Customers:** 4,372 unique customers
- **Period:** Dec 2010 – Dec 2011
- **Origin:** UK-based online retail company

---

## 🖥️ Frontend Tabs

1. **📊 Dashboard** — KPI cards + revenue trend + country map
2. **📈 Revenue Trends** — Monthly revenue & order volume dual-axis chart
3. **🛒 Top Products** — Revenue and quantity by product
4. **🌍 Geography** — Choropleth world map + pie chart
5. **👥 Customers** — RFM scatter plots + histograms + table
6. **🤖 Predict** — Interactive prediction form with confidence gauge
7. **📉 Model Insights** — Feature importance + architecture docs
