import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

TRAIN_END_DATE = '2021-12-31'
VAL_START_DATE = '2022-01-01'
VAL_END_DATE = '2022-12-31'

def seasonal_naive_model(df, seasonal_length):
    # 1. Chuẩn hóa và tạo mô hình Seasonal Naive
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df['naive_revenue'] = df['revenue'].shift(seasonal_length)

    # 2. Phân chia tập Train / Validation
    train = df[df['date'] <= TRAIN_END_DATE].copy()
    val = df[(df['date'] >= VAL_START_DATE) & (df['date'] <= VAL_END_DATE)].copy()

    # 3. Tính toán 4 chỉ số trên tập Validation
    val_clean = val.dropna(subset=['revenue', 'naive_revenue'])

    mae = mean_absolute_error(val_clean['revenue'], val_clean['naive_revenue'])
    rmse = np.sqrt(mean_squared_error(val_clean['revenue'], val_clean['naive_revenue']))
    mape = mean_absolute_percentage_error(val_clean['revenue'], val_clean['naive_revenue']) * 100
    r2 = r2_score(val_clean['revenue'], val_clean['naive_revenue'])

    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R-squared': r2
    }

    return val_clean, metrics

def linear_regression_model(df, feature_cols, target_col='revenue'):
    """
    Hàm đánh giá mô hình Baseline Linear Regression đơn giản.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu đã feature engineering.
        Bắt buộc có cột 'date', target_col, và feature_cols.

    feature_cols : list
        Danh sách cột feature dùng để train model.

    target_col : str, default='revenue'
        Tên cột target.

    Returns
    -------
    val_clean : pd.DataFrame
        Validation set kèm cột dự đoán 'lr_revenue'

    model : LinearRegression
        Model đã train

    metrics : dict
        MAE, RMSE, MAPE, R-squared
    """

    # Copy để tránh warning
    df = df.copy()

    # Chuẩn hóa date
    df['date'] = pd.to_datetime(df['date'])

    # Sort theo thời gian
    df = df.sort_values('date').reset_index(drop=True)

    # Bỏ NaN (do lag feature thường sinh NaN)
    df = df.dropna().reset_index(drop=True)

    # Split train / validation
    train = df[df['date'] <= TRAIN_END_DATE].copy()
    val = df[(df['date'] >= VAL_START_DATE) & (df['date'] <= VAL_END_DATE)].copy()

    # Tạo X / y
    X_train = train[feature_cols]
    y_train = train[target_col]

    X_val = val[feature_cols]
    y_val = val[target_col]

    # Baseline Linear Regression basic params
    model = LinearRegression(random_state=42, fit_intercept=True, n_jobs=None)

    # Train
    model.fit(X_train, y_train)

    # Predict
    val_clean = val.copy()
    val_clean['lr_revenue'] = model.predict(X_val)

    # Nếu revenue không âm thì có thể chặn âm (optional)
    # val_clean['lr_revenue'] = val_clean['lr_revenue'].clip(lower=0)

    # Metrics
    mae = mean_absolute_error(y_val, val_clean['lr_revenue'])
    rmse = np.sqrt(mean_squared_error(y_val, val_clean['lr_revenue']))
    mape = mean_absolute_percentage_error(y_val, val_clean['lr_revenue']) * 100
    r2 = r2_score(y_val, val_clean['lr_revenue'])

    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R-squared': r2
    }

    return val_clean, model, metrics