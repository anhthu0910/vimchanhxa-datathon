-- =========================================================================
-- BƯỚC 1: TẠO CÁC BẢNG MASTER (DỮ LIỆU THAM CHIẾU)
-- =========================================================================

-- 1. Bảng Địa lý (geography)
DROP TABLE IF EXISTS geography CASCADE;
CREATE TABLE IF NOT EXISTS geography (
    zip INT PRIMARY KEY,
    city VARCHAR(255),
    region VARCHAR(255),
    district VARCHAR(255)
);

-- 2. Bảng Khách hàng (customers)
DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    zip INT,
    city VARCHAR(255),
    signup_date DATE,
    gender VARCHAR(50),
    age_group VARCHAR(50),
    acquisition_channel VARCHAR(255),
    CONSTRAINT fk_cust_geo FOREIGN KEY (zip) REFERENCES geography(zip)
);

-- 3. Bảng Sản phẩm (products)
DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    segment VARCHAR(255),
    size VARCHAR(50),
    color VARCHAR(50),
    price NUMERIC,
    cogs NUMERIC,
    CONSTRAINT chk_cogs_price CHECK (cogs < price)
);

-- 4. Bảng Khuyến mãi (promotions)
DROP TABLE IF EXISTS promotions CASCADE;
CREATE TABLE IF NOT EXISTS promotions (
    promo_id VARCHAR(50) PRIMARY KEY,
    promo_name VARCHAR(255),
    promo_type VARCHAR(50),
    discount_value NUMERIC,
    start_date DATE,
    end_date DATE,
    applicable_category VARCHAR(255),
    promo_channel VARCHAR(255),
    stackable_flag INT,
    min_order_value NUMERIC
);

-- =========================================================================
-- BƯỚC 2: TẠO CÁC BẢNG TRANSACTION (GIAO DỊCH)
-- =========================================================================

-- 5. Bảng Đơn hàng (orders)
DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    zip INT,
    order_status VARCHAR(50),
    payment_method VARCHAR(100),
    device_type VARCHAR(100),
    order_source VARCHAR(100),
    CONSTRAINT fk_order_cust FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_order_geo FOREIGN KEY (zip) REFERENCES geography(zip)
);

-- 6. Bảng Chi tiết Đơn hàng (order_items)
DROP TABLE IF EXISTS order_items CASCADE;
CREATE TABLE IF NOT EXISTS order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price NUMERIC,
    discount_amount NUMERIC,
    promo_id VARCHAR(50),
    promo_id_2 VARCHAR(50),
    CONSTRAINT fk_item_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_item_prod FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_item_promo1 FOREIGN KEY (promo_id) REFERENCES promotions(promo_id),
    CONSTRAINT fk_item_promo2 FOREIGN KEY (promo_id_2) REFERENCES promotions(promo_id)
);

-- 7. Bảng Thanh toán (payments) 
DROP TABLE IF EXISTS payments CASCADE;
CREATE TABLE IF NOT EXISTS payments (
    order_id INT PRIMARY KEY,
    payment_method VARCHAR(100),
    payment_value NUMERIC,
    installments INT,
    CONSTRAINT fk_pay_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 8. Bảng Vận chuyển (shipments)
DROP TABLE IF EXISTS shipments CASCADE;
CREATE TABLE IF NOT EXISTS shipments (
    order_id INT PRIMARY KEY,
    ship_date DATE,
    delivery_date DATE,
    shipping_fee NUMERIC,
    CONSTRAINT fk_ship_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 9. Bảng Trả hàng (returns)
DROP TABLE IF EXISTS returns CASCADE;
CREATE TABLE IF NOT EXISTS returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id INT,
    product_id INT,
    return_date DATE,
    return_reason VARCHAR(255),
    return_quantity INT,
    refund_amount NUMERIC,
    CONSTRAINT fk_ret_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_ret_prod FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 10. Bảng Đánh giá (reviews)
DROP TABLE IF EXISTS reviews CASCADE;
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id INT,
    product_id INT,
    customer_id INT,
    review_date DATE,
    rating INT,
    review_title VARCHAR(255),
    CONSTRAINT fk_rev_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_rev_prod FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_rev_cust FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- =========================================================================
-- BƯỚC 3: TẠO CÁC BẢNG OPERATIONAL & ANALYTICAL
-- =========================================================================

-- 11. Bảng Tồn kho (inventory)
DROP TABLE IF EXISTS inventory CASCADE;
CREATE TABLE IF NOT EXISTS inventory (
    snapshot_date DATE,
    product_id INT,
    stock_on_hand INT,
    units_received INT,
    units_sold INT,
    stockout_days INT,
    days_of_supply NUMERIC,
    fill_rate NUMERIC,
    stockout_flag INT,
    overstock_flag INT,
    reorder_flag INT,
    sell_through_rate NUMERIC,
    product_name VARCHAR(255),
    category VARCHAR(255),
    segment VARCHAR(255),
    year INT,
    month INT,
    PRIMARY KEY (snapshot_date, product_id),
    CONSTRAINT fk_inv_prod FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 12. Bảng Dữ liệu Doanh thu (sales)
DROP TABLE IF EXISTS sales CASCADE;
CREATE TABLE IF NOT EXISTS sales (
    date DATE,
    revenue NUMERIC,
    cogs NUMERIC
);

-- 13. Bảng Lưu lượng truy cập (web_traffic)
DROP TABLE IF EXISTS web_traffic CASCADE;
CREATE TABLE IF NOT EXISTS web_traffic (
    date DATE,
    sessions INT,
    unique_visitors INT,
    page_views INT,
    bounce_rate NUMERIC,
    avg_session_duration_sec NUMERIC,
    traffic_source VARCHAR(255)
);