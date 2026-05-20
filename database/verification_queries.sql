-- verification_queries.sql
-- Queries to verify data integrity after load

-- 1. Count reviews per bank
SELECT 
    b.bank_name, 
    COUNT(r.review_id) AS total_reviews
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY total_reviews DESC;

-- 2. Compute average rating per bank
SELECT 
    b.bank_name, 
    ROUND(AVG(r.rating)::numeric, 2) AS average_rating
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY average_rating DESC;

-- 3. Check for nulls in key columns
SELECT 
    COUNT(*) AS total_missing_text
FROM reviews 
WHERE review_text IS NULL OR review_text = '';

SELECT 
    COUNT(*) AS total_missing_rating
FROM reviews 
WHERE rating IS NULL;

-- 4. Count of sentiment labels per bank
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) as sentiment_count
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, sentiment_count DESC;
