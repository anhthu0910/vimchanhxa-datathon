# scripts/database.py
import duckdb
import os
from pathlib import Path

def setup_database():
    # 1. Định vị các thư mục
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    db_dir = repo_root / "data" / "database"
    sql_dir = repo_root / "database"
    
    # Tạo thư mục chứa database nếu chưa có
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "datathon.duckdb"

    # 2. Kết nối và thực thi
    print(f"--- Đang khởi tạo database tại: {db_path} ---")
    con = duckdb.connect(str(db_path))

    try:
        # Chạy Schema
        print("1. Đang tạo cấu trúc bảng (schema.sql)...")
        con.execute((sql_dir / "schema.sql").read_text())

        # Chạy Seed (Nạp dữ liệu từ data/raw)
        print("2. Đang nạp dữ liệu từ CSV (seed.sql)...")
        # Chuyển CWD về root để lệnh COPY trong SQL tìm thấy folder data/raw
        os.chdir(repo_root)
        con.execute((sql_dir / "seed.sql").read_text())

        # Chạy Index
        print("3. Đang tối ưu hóa với chỉ mục (index.sql)...")
        con.execute((sql_dir / "index.sql").read_text())

        print("\n✅ Thành công! File database đã sẵn sàng.")
    except Exception as e:
        print(f"❌ Lỗi trong quá trình khởi tạo: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    setup_database()