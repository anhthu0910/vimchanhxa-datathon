# TỔNG QUAN DỰ ÁN 

**Mục tiêu:** 

---

## 🚀 Cài đặt và chạy

### 1. Yêu cầu hệ thống
- Python 3.12 

### 2. Chuẩn bị môi trường
```bash
# Clone repositories
git clone <repo-url>
cd vinchanhxa-datathon

# Tạo và kích hoạt virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Cài đặt thư viện
pip install -r requirements.txt
```

### 3. Tải raw data từ kaggle
```bash
python scripts/download_data.py # Windows
# python3 scripts/download_data.py # Linux/Mac
```

### 4. Thiết lập database
```bash
python scripts/database.py # Windows
# python3 scripts/database.py # Linux/Mac
```

### 5. Kiểm tra kết nối DB với jupyter notebook
Chọn Run all file `01_answer_questions.ipynb`. Nếu không có lỗi xảy ra thì tức là DB đã được kết nối thành công.


## 📊 Techstack
### Đề bài
File: /docs/Đề thi Vòng 1.pdf

### Dữ liệu thô
- Folder: data/raw/* (hiển thị sau khi run `scripts/download_data.py` thành công)
- Dữ liệu trong folder này là dữ liệu thô, chưa được xử lý.

### Database
- File: data/database/datathon.duckdb (hiển thị sau khi run `scripts/database.py` thành công)
- CSDL đã được thiết lập, có thể sử dụng để truy vấn dữ liệu.

### Kỹ thuật
- **Data Processing**: Pandas, duckdb
- **Visualization**: Matplotlib


## 🤝 Cách đóng góp vào repositories

1. Fork dự án


2. Tạo branch mới 
```bash
git checkout -b <branch-name>
```
<branch-name> đặt theo cú pháp: <role>-<member-name> (ví dụ: database-Dai, mcq-Giang,...)


3. Commit thay đổi 
```bash
git commit -m '<commit-message>'
```
**commit-message** khuyến khích đặt theo cú pháp sau cho chuyên nghiệp nhé:
`<type>(<scope>): <subject>`
- **Type - Loại commit**:
    - feat: Tính năng mới (feature).
    - fix: Sửa lỗi (bug fix).
    - docs: Thay đổi tài liệu (documentation).
    - style: Thay đổi định dạng, không ảnh hưởng code (white-space, formatting...).
    - refactor: Sửa code không phải fix bug cũng không thêm tính năng.
    - perf: Cải thiện hiệu năng.
    - test: Thêm hoặc sửa test.
    - chore: Cập nhật build task, package manager....
- **Scope - Phạm vi (optional)**: Nơi thay đổi (ví dụ: api, ui, config).
- **Subject - Mô tả**: Mô tả ngắn gọn thay đổi, tiếng Anh hay tiếng Việt đều oke.
*Ví dụ*: feat(README.md): add tutorials for new members

4. Push lên branch 
```bash
git push origin <branch-name>
```

5. Họp thường xuyên để bàn và chốt merge vào main


## 📂 Cấu trúc dự án

```
vinchanhxa-datathon/
├── data/                        # Dữ liệu đầu vào
│   └── database/                # Database (hiển thị sau khi run script database.py)
│   └── raw/                     # Dữ liệu thô (hiển thị sau khi run download_data.py)
├── database/                    # CSDL
│   ├── index.sql
│   ├── schema.sql
│   └── seed.sql  
├── docs/                        # Tài liệu của dự án
│   └── Đề thi vòng 1.pdf
├── notebooks/                   # Notebook trình bày các câu trả lời, 
│   └── 01_answer_questions.ipynb        # Hiện đang để test kết nối DB
├── src/                         # Source code
│   ├── __pycache__/             # Cache của python
│   └── connection.py            # Code kết nối DB
├── .gitignore                   # Các file bị ignore bao gồm data raw và virtual environment
├── .python-version              # Version python sẽ dùng để chạy repo này                    
├── README.md                    
└── requirements.txt             # Các thư viện cần thiết cho dự án
```

**Lưu ý:** 
- Luôn update cấu trúc folder nếu có thay đổi. Nếu không muốn push file hoặc folder đó lên github thì thêm vào file `.gitignore`.
- Cập nhật thư viện tại file `requirements.txt` nếu có thêm thư viện.