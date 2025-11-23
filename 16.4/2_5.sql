-- 2_5.sql
SELECT DISTINCT
    C1.cust_name AS "خریدار اول",
    C2.cust_name AS "خریدار دوم"
FROM
    Customer C1
INNER JOIN 
    Customer C2 
    ON C1.city = C2.city             -- شرط: زندگی در یک شهر
    AND C1.manager_id = C2.manager_id  -- شرط: داشتن یک مدیر
    AND C1.cust_id < C2.cust_id;     -- شرط: برای اطمینان از جفت‌های منحصر به فرد و حذف جفت‌های تکراری (A, B) و (B, A)
