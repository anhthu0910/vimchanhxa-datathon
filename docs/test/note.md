1. Gộp 2 file eda thành 1 kết hợp làm sạch, thay vào file Processing. Còn file thứ 3 sẽ là feature selection
2. vẽ xuyên suốt 10 năm, xem có tính gì gì, đặc điểm ra sao, vì sao lại vậy (ví dụ: tầm trước tết hay mua nhiều)
3. Kiểm tra và giải thích vì sao từ 2018-2019 revenue lại sụt
4. Phóng to lên 2 năm để thấy đoạn đầu năm và cuối năm đang có đoạn vọt lên, có thể là trùng với gần tết, nhưng cứ check lại. Kiểm tra xem trong khoảng thời gian đó liệu nó có đang ảnh hưởng tới hành vi mua hàng của khách hàng không. Đoạn vọt lên đấy có thể là trước tết, vì sau đấy khả năng nghỉ bán (nếu đúng thì thêm feat is_tet_holiday) hoặc do người mua đã nghỉ tết, ko còn mua.
5. Tiếp tục khai thác trong 2 năm đấy còn có đặc điểm gì nữa
6. xóa feat rolling_mean_90 (quý) theo bài cũ của đại

