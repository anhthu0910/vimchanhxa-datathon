-- database/seed.sql
-- =========================================================================
-- IMPORT DỮ LIỆU TỪ THƯ MỤC data/raw
-- =========================================================================

COPY geography FROM 'data/raw/geography.csv' (HEADER, DELIMITER ',');
COPY products FROM 'data/raw/products.csv' (HEADER, DELIMITER ',');
COPY customers FROM 'data/raw/customers.csv' (HEADER, DELIMITER ',');
COPY promotions FROM 'data/raw/promotions.csv' (HEADER, DELIMITER ',');

COPY orders FROM 'data/raw/orders.csv' (HEADER, DELIMITER ',');
COPY order_items FROM 'data/raw/order_items.csv' (HEADER, DELIMITER ',');
COPY payments FROM 'data/raw/payments.csv' (HEADER, DELIMITER ',');
COPY shipments FROM 'data/raw/shipments.csv' (HEADER, DELIMITER ',');
COPY returns FROM 'data/raw/returns.csv' (HEADER, DELIMITER ',');
COPY reviews FROM 'data/raw/reviews.csv' (HEADER, DELIMITER ',');

COPY inventory FROM 'data/raw/inventory.csv' (HEADER, DELIMITER ',');
COPY sales FROM 'data/raw/sales.csv' (HEADER, DELIMITER ',');
COPY web_traffic FROM 'data/raw/web_traffic.csv' (HEADER, DELIMITER ',');