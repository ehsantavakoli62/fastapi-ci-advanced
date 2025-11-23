-- 2_2.sql
SELECT
    C.cust_name AS "نام خریدار بدون سفارش"
FROM
    Customer C
LEFT JOIN 
    Orders O ON C.cust_id = O.cust_id
WHERE
    O.order_id IS NULL; -- سفارشاتی که در جدول Orders مطابقت ندارند
