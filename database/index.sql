-- =========================================================================
-- TẠO CHỈ MỤC (INDEX) CHO CÁC KHÓA NGOẠI THƯỜNG XUYÊN JOIN
-- =========================================================================
-- Lưu ý: Hãy chạy seed trước khi chạy file index
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_returns_order_id ON returns(order_id);
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_order_items_promo_id_2 ON order_items(promo_id_2);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_web_traffic_date ON web_traffic(date);
CREATE INDEX idx_inventory_snapshot_date ON inventory(snapshot_date);