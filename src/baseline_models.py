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

def evaluate_vanilla_lightgbm(df, features_col, target_col='revenue', 
                              train_end='2021-12-31', 
                              val_start='2022-01-01', 
                              val_end='2022-12-31'):
    """
    Hàm đánh giá mô hình Vanilla LightGBM làm Baseline.
    df: DataFrame chứa các đặc trưng đã được xử lý.
    """
    # Tránh cảnh báo SettingWithCopyWarning bằng cách copy df gốc
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Bỏ dòng NaN trước khi chia split (do lag có thể sinh ra NaN)
    df = df.dropna().reset_index(drop=True)

    train = df[df['date'] <= train_end].copy()
    val = df[(df['date'] >= val_start) & (df['date'] <= val_end)].copy()

    X_train = train[features_col]
    y_train = train[target_col]
    
    X_val = val[features_col]
    y_val = val[target_col]

    # Huấn luyện mô hình LightGBM với các tham số mặc định (Vanilla)
    model = lgb.LGBMRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Dự đoán trên tập Validation
    val_clean = val.copy()
    val_clean['lgbm_revenue'] = model.predict(X_val)

    # Tính toán 4 chỉ số
    mae = mean_absolute_error(val_clean[target_col], val_clean['lgbm_revenue'])
    rmse = np.sqrt(mean_squared_error(val_clean[target_col], val_clean['lgbm_revenue']))
    mape = mean_absolute_percentage_error(val_clean[target_col], val_clean['lgbm_revenue']) * 100
    r2 = r2_score(val_clean[target_col], val_clean['lgbm_revenue'])

    return val_clean, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R-squared': r2}
