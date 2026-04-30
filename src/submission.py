# Tạo submission cho bài toán dự đoán doanh thu tháng 1/2023
OUTPUT_PATH = '../data/processed/submission.csv'

def create_submission(model, test_df, feature_cols, output_path=OUTPUT_PATH):
    """
    Tạo file submission.csv với 2 cột: date và revenue.
    model: Mô hình đã được huấn luyện.
    test_df: DataFrame chứa dữ liệu test (tháng 1/2023) với cột 'date' và các đặc trưng.
    feature_cols: Danh sách tên các cột đặc trưng để dự đoán.
    output_path: Đường dẫn lưu file submission.csv.
    """
    # Chuẩn bị dữ liệu test
    X_test = test_df[feature_cols]
    
    # Dự đoán doanh thu
    test_df['revenue'] = model.predict(X_test)
    
    # Tạo DataFrame submission
    submission_df = test_df[['date', 'revenue']].copy()
    
    # Lưu file submission.csv
    submission_df.to_csv(output_path, index=False)
    
    print(f'Submission file saved to {output_path}')
    return submission_df