import pandas as pd
import duckdb
from pathlib import Path

def get_connection(read_only=True):
    """
    Trả về đối tượng kết nối DuckDB tới file datathon.duckdb.
    Mặc định mở ở chế độ read_only để tránh hỏng dữ liệu khi dùng nhiều nơi.
    """
    # Tìm đường dẫn tới file .duckdb dựa trên vị trí của file connection.py
    current_dir = Path(__file__).resolve().parent
    repo_root = current_dir.parent
    db_path = repo_root / "data" / "database" / "datathon.duckdb"

    if not db_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file database tại {db_path}. "
            "Vui lòng chạy 'python scripts/database.py' trước!"
        )

    print(f"[OKE] Kết nối thành công tới database tại {db_path}")
    return duckdb.connect(str(db_path), read_only=read_only)


def get_data_processed(filename):
    """
    Đọc dữ liệu đã được xử lý từ thư mục data/processed.
    filename: tên file (ví dụ: 'sales_features.csv')
    Trả về DataFrame chứa dữ liệu đã đọc.
    """
    repo_root = Path(__file__).resolve().parents[1]
    processed_dir = repo_root / 'data' / 'processed'
    file_path = processed_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file {file_path}. Vui lòng kiểm tra lại tên file và thư mục.")

    try:
        df = pd.read_csv(file_path)
        print(f"Đã đọc thành công dữ liệu từ: {file_path}")
        return df
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return None