-- 2_3.sql
SELECT
    O.order_id AS "شماره سفارش",
    S.seller_name AS "نام فروشنده",
    C.cust_name AS "نام خریدار"
FROM
    Orders O
INNER JOIN 
    Customer C ON O.cust_id = C.cust_id
INNER JOIN 
    Seller S ON O.seller_id = S.seller_id
WHERE
    C.city <> S.city; -- فیلتر بر اساس عدم تطابق شهر
