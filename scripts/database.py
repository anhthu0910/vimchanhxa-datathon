# scripts/database.py
import duckdb
import os
from pathlib import Path

def get_connection():
    """Get a connection to the DuckDB database."""
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    db_path = repo_root / "data" / "database" / "datathon.duckdb"
    return duckdb.connect(str(db_path))

def setup_database():
    # 1. Determine the path to the database files
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    db_dir = repo_root / "data" / "database"
    sql_dir = repo_root / "database"
    
    # Create the directory to store the database if it doesn't exist
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "datathon.duckdb"

    # Remove old database file if it exists
    if db_path.exists():
        db_path.unlink()
        print(f"Đã xóa file database cũ: {db_path}")

    # 2. Connect and execute
    print(f"--- Initializing database at: {db_path} ---")
    con = duckdb.connect(str(db_path))

    try:
        # Run Schema
        print("1. Creating table structure (schema.sql)...")
        con.execute((sql_dir / "schema.sql").read_text(encoding="utf-8"))

        # Run Seed (Load data from data/raw)
        print("2. Loading data from CSV (seed.sql)...")
        # Change CWD to root so that the COPY command in SQL can find the data/raw folder
        os.chdir(repo_root)
        con.execute((sql_dir / "seed.sql").read_text(encoding="utf-8"))

        # Run Index
        print("3. Optimizing with indexes (index.sql)...")
        con.execute((sql_dir / "index.sql").read_text(encoding="utf-8"))

        print("\n✅ Success! The database file is ready.")
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    setup_database()