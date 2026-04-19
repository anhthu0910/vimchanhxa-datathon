-- =========================================================================
-- BƯỚC 1: IMPORT BẢNG MASTER (BẮT BUỘC CHẠY TRƯỚC)
-- =========================================================================
COPY geography FROM 'C:\datathon-2026\geography.csv' DELIMITER ',' CSV HEADER;
COPY products FROM 'C:\datathon-2026\products.csv' DELIMITER ',' CSV HEADER;
COPY customers FROM 'C:\datathon-2026\customers.csv' DELIMITER ',' CSV HEADER;
COPY promotions FROM 'C:\datathon-2026\promotions.csv' DELIMITER ',' CSV HEADER;

-- =========================================================================
-- BƯỚC 2: IMPORT BẢNG TRANSACTION
-- =========================================================================
COPY orders FROM 'C:\datathon-2026\orders.csv' DELIMITER ',' CSV HEADER;
COPY order_items FROM 'C:\datathon-2026\order_items.csv' DELIMITER ',' CSV HEADER;
COPY payments FROM 'C:\datathon-2026\payments.csv' DELIMITER ',' CSV HEADER;
COPY shipments FROM 'C:\datathon-2026\shipments.csv' DELIMITER ',' CSV HEADER;
COPY returns FROM 'C:\datathon-2026\returns.csv' DELIMITER ',' CSV HEADER;
COPY reviews FROM 'C:\datathon-2026\reviews.csv' DELIMITER ',' CSV HEADER;

-- =========================================================================
-- BƯỚC 3: IMPORT BẢNG OPERATIONAL & ANALYTICAL
-- =========================================================================
COPY inventory FROM 'C:\datathon-2026\inventory.csv' DELIMITER ',' CSV HEADER;
COPY sales FROM 'C:\datathon-2026\sales.csv' DELIMITER ',' CSV HEADER;
COPY web_traffic FROM 'C:\datathon-2026\web_traffic.csv' DELIMITER ',' CSV HEADER;
