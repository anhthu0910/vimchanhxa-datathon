import requests
import zipfile
from pathlib import Path

def download_and_extract_data(url: str):
    # 1. Xác định đường dẫn thư mục gốc (repo root)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    target_dir = repo_root / "data" / "raw"
    
    # Tạo thư mục data/raw nếu nó chưa tồn tại
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Đường dẫn để lưu file zip tạm thời
    zip_path = target_dir / "datathon-2026-round-1.zip"
    
    print("Đang tải dữ liệu từ URL...")
    
    # 2. Tải file về (dùng stream=True để không làm tràn RAM với file lớn)
    response = requests.get(url, stream=True)
    response.raise_for_status() # Báo lỗi nếu link hỏng hoặc bị chặn
    
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                
    print("Tải xong! Đang tiến hành giải nén...")
    
    # 3. Giải nén file zip vào data/raw
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        
    # 4. Xóa file zip rác sau khi giải nén xong
    zip_path.unlink()
    
    print(f"\n✅ Hoàn tất! Dữ liệu đã sẵn sàng tại thư mục: {target_dir}")

if __name__ == "__main__":
    # Link tải trực tiếp của bạn
    DOWNLOAD_URL = "https://storage.googleapis.com/kaggle-competitions-data/kaggle-v2/137414/16735012/bundle/archive.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1776694733&Signature=Wvk8FFmGq5JL4P9cyEHMvLBVElREIyslLxgq7D7SSO1hv4gv16TOPJluXsWRrwk19iSeYf3DecVRKVw8pBUe%2FuC58n9WdhZHPheeu1HH8fAWfP7yRGa4ek6fk5eh34%2BXYOdZs6edmm1CP6ciw%2FFnA%2B%2FpA9DWf3sg%2BfdRhqlv8tXD5UQ%2BpVJsxAofO8EFUjHGYYGgbrT1mGHcW5buQ5JH3mOSfqTw%2BlbxS8Bn5dbrC9AX0JqKP58CTx3rY5fJZPcIabjMgnCG2ehD%2FdLstd68%2FccTOgqi%2BsYescn%2FplLFCLyJva3ujE6jTdR7BVtM9RA28iI6OGavEyWGBHVFsGY4IQ%3D%3D&response-content-disposition=attachment%3B+filename%3Ddatathon-2026-round-1.zip"
    
    download_and_extract_data(DOWNLOAD_URL)