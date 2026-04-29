import optuna
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
import numpy as np

# Giả sử bạn đã có:
# X_train, y_train (Dữ liệu huấn luyện)
# X_val, y_val (Dữ liệu validation - rất quan trọng trong time series, thường là những tháng cuối cùng)

def objective(trial):
    # 1. Định nghĩa không gian tìm kiếm (Search Space)
    param = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'verbosity': -1,
        
        # Cho Optuna tự chọn các giá trị trong khoảng này:
        'learning_rate': trial.suggest_float('learning_rate', 0.005, 0.1, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 15, 100),
        'max_depth': trial.suggest_int('max_depth', 4, 12),
        
        # Tham số trị lag_364: Ép Optuna tìm tỷ lệ lấy mẫu feature tốt nhất (từ 40% đến 80%)
        'feature_fraction': trial.suggest_float('feature_fraction', 0.4, 0.8),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.5, 0.95),
        'bagging_freq': trial.suggest_int('bagging_freq', 1, 5),
        
        'min_child_samples': trial.suggest_int('min_child_samples', 10, 100),
        'lambda_l1': trial.suggest_float('lambda_l1', 1e-8, 10.0, log=True),
        'lambda_l2': trial.suggest_float('lambda_l2', 1e-8, 10.0, log=True),
    }

    df = df_seasonals.copy()  # Sử dụng df_seasonals đã được xử lý và có đầy đủ features
    df = df.sort_values('date')  # Đảm bảo dữ liệu được sắp xếp theo thời gian
    df = df.drop(columns=['cogs'], errors='ignore')  # Đảm bảo cột cogs đã bị xóa (nếu chưa xóa ở bước trước)
    df = df.dropna()  # Đảm bảo không có giá trị thiếu (nếu có)

    X_train = df[feature_cols].iloc[:-12]  # Dữ liệu huấn luyện (tất cả trừ 12 tháng cuối)
    y_train = df[target_col].iloc[:-12]

    X_val = df[feature_cols].iloc[-12:]  # Dữ liệu validation (12 tháng cuối)
    y_val = df[target_col].iloc[-12:]

    # 2. Khởi tạo dataset cho LightGBM
    dtrain = lgb.Dataset(X_train, label=y_train)
    dval = lgb.Dataset(X_val, label=y_val, reference=dtrain)

    # 3. Huấn luyện mô hình
    # Lặp 1000 vòng (num_boost_round), dừng sớm nếu sau 50 vòng không cải thiện trên tập validation
    model = lgb.train(
        param,
        dtrain,
        valid_sets=[dval],
        num_boost_round=1000,
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
    )

    # 4. Đánh giá và trả về lỗi
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    return rmse

# --- BẮT ĐẦU CHẠY OPTUNA ---
study = optuna.create_study(direction='minimize') # Minimize vì chúng ta muốn RMSE nhỏ nhất
study.optimize(objective, n_trials=50) # Chạy thử 50 bộ tham số khác nhau (tăng lên 100-200 nếu có thời gian)

# --- IN RA KẾT QUẢ TỐT NHẤT ---
print("Bộ tham số tốt nhất:", study.best_params)
print("RMSE tốt nhất:", study.best_value)

# Lấy bộ tham số này để train mô hình cuối cùng:
best_params = study.best_params
best_params['objective'] = 'regression'
best_params['metric'] = 'rmse'
best_params['boosting_type'] = 'gbdt'
# ... (Dùng best_params để train lại bằng lgb.train trên toàn bộ tập dữ liệu)