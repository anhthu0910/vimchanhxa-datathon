# CÁC HƯỚNG MODEL:

## 1. Dự đoán theo các **Demand decomposition models**
**Công thức**:
```
Revenue = Traffic × Conversion Rate × AOV
```
Trong đó, phải train 3 model để dự đoán:

- **Model 1: Traffic (sessions)**

→ từ web_traffic (time series + seasonality)

- **Model 2: Conversion Rate**
```
orders / sessions 
```

- **Model 3: AOV (average order value)**
```
Revenue / orders
```
Sau đó nhân output của 3 model lại để ra Revenue.

**FEATURE ENGINEERING:**

🕒 Time features

- day_of_week
- week_of_year
- month
- holiday_flag

- Demand drivers

sessions, users (web_traffic)

promo_active_flag

discount_level (avg)

- Pricing

avg price

avg discount

- Supply side

stockout_rate

fill_rate

- Behavior

return_rate

avg rating

## 2. Build **category-level model** + ensemble với ML model (LightGBM):

