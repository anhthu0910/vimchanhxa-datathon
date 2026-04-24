import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

def evaluate_seasonal_naive_model(df, seasonal_length):
    # 1. Chuẩn hóa và tạo mô hình Seasonal Naive
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df['naive_revenue'] = df['revenue'].shift(seasonal_length)

    # 2. Phân chia tập Train / Validation
    train = df[df['date'] <= '2021-12-31'].copy()
    val = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2022-12-31')].copy()

    # 3. Tính toán 4 chỉ số trên tập Validation
    val_clean = val.dropna(subset=['revenue', 'naive_revenue'])

    mae = mean_absolute_error(val_clean['revenue'], val_clean['naive_revenue'])
    rmse = np.sqrt(mean_squared_error(val_clean['revenue'], val_clean['naive_revenue']))
    mape = mean_absolute_percentage_error(val_clean['revenue'], val_clean['naive_revenue']) * 100
    r2 = r2_score(val_clean['revenue'], val_clean['naive_revenue'])

    return val_clean, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R-squared': r2}

def evaluate_vanilla_lightgbm(df):
    """
    Hàm đánh giá mô hình Vanilla LightGBM làm Baseline.
    Sử dụng các đặc trưng thời gian và lag cơ bản.
    """
    # Tránh cảnh báo SettingWithCopyWarning bằng cách copy df gốc
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Đặc trưng thời gian tĩnh
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month

    # Đặc trưng chu kỳ (Lags) - Kết hợp cả chu kỳ Tuần và chu kỳ Năm
    df['lag_7'] = df['revenue'].shift(7)
    df['lag_30'] = df['revenue'].shift(30)
    df['lag_120'] = df['revenue'].shift(120)
    df['lag_364'] = df['revenue'].shift(364)

    # Loại bỏ các dòng bị NaN do hàm shift tạo ra (sẽ mất 364 ngày đầu tiên của tập Train)
    df = df.dropna().reset_index(drop=True)

    train = df[df['date'] <= '2021-12-31'].copy()
    val = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2022-12-31')].copy()

    # Định nghĩa biến đầu vào (X) và biến mục tiêu (y)
    features = ['day_of_week', 'month', 'lag_7', 'lag_30', 'lag_120', 'lag_364']
    target = 'revenue'

    X_train = train[features]
    y_train = train[target]
    
    X_val = val[features]
    y_val = val[target]

    # Huấn luyện mô hình LightGBM với các tham số mặc định (Vanilla)
    # Thiết lập random_state=42 để đảm bảo tính "Tái lập" (Reproducibility) theo yêu cầu đề thi
    model = lgb.LGBMRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Dự đoán trên tập Validation
    val_clean = val.copy()
    val_clean['lgbm_revenue'] = model.predict(X_val)

    # Tính toán 4 chỉ số
    mae = mean_absolute_error(val_clean['revenue'], val_clean['lgbm_revenue'])
    rmse = np.sqrt(mean_squared_error(val_clean['revenue'], val_clean['lgbm_revenue']))
    mape = mean_absolute_percentage_error(val_clean['revenue'], val_clean['lgbm_revenue']) * 100
    r2 = r2_score(val_clean['revenue'], val_clean['lgbm_revenue'])

    return val_clean, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R-squared': r2}
