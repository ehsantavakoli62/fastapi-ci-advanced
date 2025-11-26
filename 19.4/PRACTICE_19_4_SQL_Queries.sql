-- 1. یافتن سخت‌ترین معلم (پایین‌ترین میانگین نمرات)
SELECT
    t.name AS teacher_name,
    AVG(g.grade) AS avg_grade
FROM
    grades g
JOIN
-- ... بقیه کوئری ۱ ...
LIMIT 1;

-- 2. انتخاب ۱۰ دانش‌آموز برتر
SELECT
    s.name AS student_name,
    AVG(g.grade) AS avg_grade
FROM
-- ... بقیه کوئری ۲ ...
LIMIT 10;

-- 3. یافتن دانش‌آموزان ساده‌ترین معلم (با استفاده از JOIN)
SELECT
    s.name AS student_name
FROM
-- ... بقیه کوئری ۳ (ب) ...
    );

-- 4. آمار تکالیف عقب‌افتاده برای هر کلاس (با استفاده از JOIN)
SELECT
    c.class_name,
    AVG(g.overdue_status) AS avg_overdue,
-- ... بقیه کوئری ۴ (ب) ...
GROUP BY
    c.class_name;
