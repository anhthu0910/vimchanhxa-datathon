import numpy as np
import pandas as pd
import optuna
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from optuna.samplers import TPESampler

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
                              val_end='2022-12-31',
                              best_lgb_params=None):
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

    if best_lgb_params is None:
        best_lgb_params = dict()  # Nếu không có tham số tối ưu, sử dụng mặc định của LightGBM

    # --- Các tham số cơ bản cho bài toán Regression ---
    best_lgb_params['objective'] = 'regression'
    best_lgb_params['boosting_type'] = 'gbdt'
    best_lgb_params['random_state'] = 42
    best_lgb_params['n_jobs'] = -1
    best_lgb_params['verbose'] = -1

    # Huấn luyện mô hình LightGBM với các tham số tối ưu
    # Khởi tạo mô hình
    model = lgb.LGBMRegressor(**best_lgb_params, n_estimators=1000)
    
    # Huấn luyện có điểm dừng sớm (Early Stopping)
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)], # Đưa cả train và val vào để theo dõi
        eval_metric='rmse',
        callbacks=[
            lgb.early_stopping(stopping_rounds=50, verbose=True), # Dừng nếu sau 50 vòng RMSE không giảm
            lgb.log_evaluation(period=100) # In log mỗi 100 vòng
        ]
    )

    # Dự đoán trên tập Validation
    val_clean = val.copy()
    val_clean['lgbm_revenue'] = model.predict(X_val)

    # Tính toán 4 chỉ số
    mae = mean_absolute_error(val_clean[target_col], val_clean['lgbm_revenue'])
    rmse = np.sqrt(mean_squared_error(val_clean[target_col], val_clean['lgbm_revenue']))
    mape = mean_absolute_percentage_error(val_clean[target_col], val_clean['lgbm_revenue']) * 100
    r2 = r2_score(val_clean[target_col], val_clean['lgbm_revenue'])

    return val_clean, model, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R-squared': r2}

def get_best_lgb_params(df, features_col, target_col='revenue', n_trials=50,
                        train_end='2021-12-31', val_start='2022-01-01', val_end='2022-12-31'):
    """
    Hàm sử dụng Optuna để tìm ra các tham số tốt nhất cho LightGBM theo thời gian thực.
    n_trials: Số lượng bộ tham số muốn thử nghiệm (mặc định là 50).
    """
    # 1. Tiền xử lý và chia tập dữ liệu (Đảm bảo không rò rỉ dữ liệu tương lai)
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df = df.dropna().reset_index(drop=True)

    train = df[df['date'] <= train_end]
    val = df[(df['date'] >= val_start) & (df['date'] <= val_end)]

    X_train, y_train = train[features_col], train[target_col]
    X_val, y_val = val[features_col], val[target_col]

    # 2. Định nghĩa hàm mục tiêu để Optuna tối ưu hóa
    def objective(trial):
        param = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'verbosity': -1,
            'random_state': 42,
            'n_jobs': -1,
            
            # Không gian tìm kiếm tham số
            'learning_rate': trial.suggest_float('learning_rate', 0.005, 0.1, log=True),
            'num_leaves': trial.suggest_int('num_leaves', 15, 100),
            'max_depth': trial.suggest_int('max_depth', 4, 12),
            
            # Các tham số kiểm soát việc chọn mẫu (giúp giảm phụ thuộc vào lag)
            'feature_fraction': trial.suggest_float('feature_fraction', 0.4, 0.8),
            'bagging_fraction': trial.suggest_float('bagging_fraction', 0.5, 0.95),
            'bagging_freq': trial.suggest_int('bagging_freq', 1, 5),
            
            # Điều chuẩn
            'min_child_samples': trial.suggest_int('min_child_samples', 10, 100),
            'lambda_l1': trial.suggest_float('lambda_l1', 1e-8, 10.0, log=True),
            'lambda_l2': trial.suggest_float('lambda_l2', 1e-8, 10.0, log=True),
        }

        # Huấn luyện mô hình trong quá trình thử nghiệm
        model = lgb.LGBMRegressor(**param, n_estimators=1000)
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            eval_metric='rmse',
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
        )

        # Đánh giá bằng RMSE trên tập Validation
        preds = model.predict(X_val)
        rmse = np.sqrt(mean_squared_error(y_val, preds))
        return rmse

    # 3. Khởi tạo và chạy quá trình tìm kiếm Optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING) # Ẩn bớt log để console gọn gàng hơn
    study = optuna.create_study(direction='minimize', sampler=TPESampler(seed = 42))
    
    print(f"Đang tiến hành tìm kiếm tham số tối ưu với {n_trials} quá trình (trials)...")
    study.optimize(objective, n_trials=n_trials)

    print("Min RMSE: {:.4f}".format(study.best_value))

    return study.best_params


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_feature_importances(model, importance_type='gain', top_n=20, plot=True):
    """
    Hàm trích xuất và trực quan hóa độ quan trọng của các đặc trưng từ mô hình LightGBM.
    
    Tham số:
    - model: Mô hình LightGBM đã được huấn luyện (VD: lgb.LGBMRegressor).
    - importance_type: 'gain' (tổng mức độ giảm lỗi) hoặc 'split' (số lần feature được dùng để chia nhánh).
    - top_n: Số lượng features quan trọng nhất muốn hiển thị/trả về.
    - plot: Nếu True, sẽ vẽ luôn biểu đồ dạng cột ngang.
    
    Trả về:
    - DataFrame chứa danh sách các features và điểm quan trọng tương ứng, đã được sắp xếp.
    """
    # Trích xuất độ quan trọng và tên đặc trưng từ mô hình
    importances = model.booster_.feature_importance(importance_type=importance_type)
    feature_names = model.booster_.feature_name()
    
    # Tạo DataFrame
    df_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    })
    
    # Sắp xếp giảm dần theo độ quan trọng
    df_importance = df_importance.sort_values(by='importance', ascending=False).reset_index(drop=True)
    
    # Lấy top N features
    df_top_n = df_importance.head(top_n)
    
    # Trực quan hóa nếu plot=True
    if plot:
        plt.figure(figsize=(10, 8))
        sns.barplot(
            x='importance', 
            y='feature', 
            data=df_top_n, 
            palette='viridis'
        )
        plt.title(f'Top {top_n} Features Quan Trọng Nhất (Theo {importance_type.upper()})')
        plt.xlabel('Điểm Quan Trọng (Importance Score)')
        plt.ylabel('Tên Đặc Trưng (Feature)')
        plt.tight_layout()
        plt.show()
        
    return df_importance