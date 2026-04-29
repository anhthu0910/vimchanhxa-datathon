import joblib
from pathlib import Path
import datetime

def save_trained_model(model, model_name):
    """
    Lưu mô hình máy học vào thư mục 'model' ở root của dự án.
    
    Tham số:
    - model: Đối tượng mô hình đã được huấn luyện (VD: final_model của LightGBM).
    - model_name (str): Tên cơ sở của file model.
    
    Trả về:
    - file_path (Path): Đường dẫn tuyệt đối tới file đã lưu.
    """
    print(f"💾 Đang tiến hành lưu mô hình '{model_name}'...")
    
    # 1. Xác định thư mục root một cách động (Dynamic Path)
    # __file__ trỏ tới src/save_model.py
    # .parent lần 1 trỏ tới thư mục 'src'
    # .parent lần 2 trỏ tới thư mục gốc (root)
    current_file_path = Path(__file__).resolve()
    root_dir = current_file_path.parent.parent
    
    # 2. Khai báo thư mục chứa model
    model_dir = root_dir / 'models'
    
    # Tạo thư mục 'models' nếu nó chưa tồn tại ở root
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. Tạo tên file có chứa Timestamp để không vô tình ghi đè model cũ
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    full_file_name = f"{model_name}_{timestamp}.pkl"
    file_path = model_dir / full_file_name
    
    # 4. Thực hiện lưu model bằng joblib
    try:
        joblib.dump(model, file_path)
        print(f"✅ Lưu model thành công!")
        print(f"📂 Vị trí: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình lưu model: {e}")
        return None