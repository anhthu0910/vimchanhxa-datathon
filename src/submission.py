# Tạo submission cho bài toán dự đoán doanh thu tháng 1/2023
OUTPUT_PATH = '../data/processed/submission.csv'

def create_submission(result, output_path=OUTPUT_PATH):
    """
    Tạo file submission.csv với 2 cột: date và revenue.
    result: Kết quả dự đoán từ mô hình.
    output_path: Đường dẫn lưu file submission.csv.
    output_path: Đường dẫn lưu file submission.csv.
    """
    # Xử lý tên cột
    result.rename(columns={
        'date': 'Date',
        'revenue': 'Revenue',
        'cogs': 'COGS'
    }, inplace=True)

    # Lưu file submission.csv
    result.to_csv(output_path, index=False)
    
    print(f'Submission file saved to {output_path}')
    return result