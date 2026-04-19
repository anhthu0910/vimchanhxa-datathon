# src/connection.py
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

    return duckdb.connect(str(db_path), read_only=read_only)