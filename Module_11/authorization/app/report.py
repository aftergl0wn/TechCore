from sqlalchemy import text

REPORT_SQL = text("""
SELECT
    a.name AS author_name,
    COUNT(b.id) AS books_count,
    MIN(b.year) AS earliest_year,
    MAX(b.year) AS lastest_year
FROM book b
LEFT JOIN author a ON b.author_id = a.id
GROUP BY a.id;
"""
)
