# PIPELINE:

- Baseline: LightGBM thuần túy trên dữ liệu thời gian (?)
- Build các model khác (tạm gọi là các model A, B)
    - Train 2 hướng model như bên dưới và đánh giá metric từng model
    - Ensemble cả 2 model tùy chỉnh trọng số rồi đánh giá metric từng trường hợp
    - Dựa theo kết quả tất cả các metric trên => Chọn ra framework tốt nhất


# CÁC MODEL CẦN BUILD THÊM:

## 1. Model A: Decomposition forecast model:

### 1.1 Ý tưởng:
Bạn không dự đoán trực tiếp Revenue nữa, mà tách nó thành các thành phần có ý nghĩa business. Bản chất của model này là tính chất *nguyên nhân - hệ quả* (Causal structure)

**Công thức**:
```
Revenue = Traffic × Conversion Rate × AOV
```

### 1.2 Cách hoạt động:
Bạn sẽ build 3 model riêng:

- **Model 1: Traffic**

Dự đoán session từ web_traffic theo thời gian

- **Model 2: Conversion Rate**

Dự đoán tỉ lệ người truy cập thật sự mua hàng (CR) từ giá trị CR theo thời gian, với công thức:
```
CR = orders / sessions * 100
```


- **Model 3: AOV (Average Order Value)**
Dự đoán giá trị trung bình mỗi đơn (AOV) từ giá trị AOV theo thời gian, với công thức
```
AOV = revenue / orders
```

- Sau đó nhân output của 3 model lại để ra giá trị Revenue dự đoán:
```
Revenue_pred = sessions_pred × conversion_pred × AOV_pred
```


## 2. Model B: Category-level model

### 2.1 Ý tưởng:
Thay vì nhìn toàn bộ revenue như 1 khối, revenue tách theo category và segment (đoạn mã 2 kí tự ở `product_name` trong `products.csv`).
```
Revenue_total = Revenue_UC + Revenue_YY + Revenue_RS + ...
```

### 2.2 Cách hoạt động:

**Bước 1:** Group data theo:
- `category_segment_id`: Đoạn mã gồm 2 kí tự in hoa đại diện cho category và segment ở product_name (`product.csv`)
- `date`: tham chiếu đến `order.csv`

**Bước 2:** Train ML model (LightGBM) predict từng category

**Bước 3:** Cộng lại thành total revenue

### 2.3 Ưu điểm:
- Bắt được pattern riêng. Ví dụ: Category Casual All-weather được mua đều xuyên suốt trong năm; Genz Trendy chỉ có doanh thu cao vào một giai đoạn; ...
- Total revenue dễ được trung bình hóa (average out) 
- Giảm bias