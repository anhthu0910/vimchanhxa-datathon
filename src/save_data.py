from pathlib import Path

def save_to_processed(data, filename):
	"""
	Lưu dữ liệu vào thư mục data/processed với tên file chỉ định.
	data: dữ liệu (DataFrame hoặc string)
	filename: tên file (ví dụ: 'output.csv')
	"""
	repo_root = Path(__file__).resolve().parents[1]
	processed_dir = repo_root / 'data' / 'processed'
	processed_dir.mkdir(parents=True, exist_ok=True)
	file_path = processed_dir / filename

	# Nếu là pandas DataFrame thì dùng to_csv, nếu là string thì ghi trực tiếp
	try:
		if hasattr(data, 'to_csv'):
			data.to_csv(file_path, index=False)
		else:
			file_path.write_text(str(data), encoding='utf-8')
		print(f"Đã lưu thành công tại: {file_path}")
	except Exception as e:
		print(f"Lỗi khi lưu file: {e}")

