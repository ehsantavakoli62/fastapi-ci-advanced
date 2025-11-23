-- 2_4.sql
SELECT
    C.cust_name AS "نام خریدار بدون مدیر",
    O.order_id AS "شماره سفارش"
FROM
    Customer C
INNER JOIN 
    Orders O ON C.cust_id = O.cust_id
WHERE
    C.manager_id IS NULL; -- خریدارانی که manager_id آن‌ها NULL است
