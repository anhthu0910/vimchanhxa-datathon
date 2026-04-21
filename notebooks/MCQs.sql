-- Câu 1:
WITH OrderGaps AS (
    -- Bước 1: Sắp xếp đơn hàng theo khách hàng và ngày, sau đó tính khoảng cách ngày
    SELECT 
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as previous_order_date,
        order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as gap
    FROM orders
    WHERE order_status = 'delivered' -- Lọc các đơn hàng thành công để kết quả chính xác hơn
)
-- Bước 2: Tính trung vị của các khoảng cách (loại bỏ giá trị NULL của đơn hàng đầu tiên)
SELECT 
    percentile_cont(0.5) WITHIN GROUP (ORDER BY gap) as median_inter_order_gap
FROM OrderGaps
WHERE gap IS NOT NULL;

--Câu 2:
SELECT 
    segment, 
    AVG((price - cogs) / price) AS avg_gross_margin
FROM products
GROUP BY segment
ORDER BY avg_gross_margin DESC;

--Câu 3:
SELECT 
    r.return_reason, 
    COUNT(*) AS reason_count
FROM returns r
JOIN products p ON r.product_id = p.product_id
WHERE p.category = 'Streetwear'
GROUP BY r.return_reason
ORDER BY reason_count DESC
LIMIT 1;

--Câu 4:
SELECT 
    traffic_source, 
    AVG(bounce_rate) AS avg_bounce_rate
FROM web_traffic
GROUP BY traffic_source
ORDER BY avg_bounce_rate ASC
LIMIT 1;

-- Câu 5:
SELECT 
    (COUNT(promo_id) * 100.0 / COUNT(*)) AS promo_percentage
FROM order_items;

--Câu 6:
SELECT 
    c.age_group, 
    COUNT(o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id) AS avg_orders_per_customer
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.age_group IS NOT NULL
GROUP BY c.age_group
ORDER BY avg_orders_per_customer DESC;

--Câu 7:
SELECT 
    g.region, 
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN geography g ON o.zip = g.zip
GROUP BY g.region
ORDER BY total_revenue DESC;

--Câu 8:
SELECT 
    payment_method, 
    COUNT(*) AS total_cancelled
FROM orders
WHERE order_status = 'cancelled'
GROUP BY payment_method
ORDER BY total_cancelled DESC
LIMIT 1;

-- Câu 9:
SELECT 
    p.size, 
    COUNT(r.return_id) * 1.0 / COUNT(oi.*) AS return_rate
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN returns r ON oi.order_id = r.order_id AND oi.product_id = r.product_id
WHERE p.size IN ('S', 'M', 'L', 'XL')
GROUP BY p.size
ORDER BY return_rate DESC;

--Câu 10:
SELECT 
    installments, 
    AVG(payment_value) AS avg_payment_amount
FROM payments
GROUP BY installments
ORDER BY avg_payment_amount DESC
LIMIT 1;