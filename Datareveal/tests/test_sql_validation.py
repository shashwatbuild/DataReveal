import unittest

from utils.sql_validation import extract_sql, validate_and_sanitize_sql


class SqlValidationTests(unittest.TestCase):
    def test_extract_sql_keeps_multiline_query_body(self):
        raw = """Here is the SQL:
SELECT
  product,
  SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
"""
        self.assertEqual(
            extract_sql(raw),
            "SELECT product, SUM(revenue) AS total_revenue FROM sales GROUP BY product ORDER BY total_revenue DESC",
        )

    def test_validate_strips_single_trailing_semicolon(self):
        result = validate_and_sanitize_sql("SELECT name FROM sales;", row_limit=50)
        self.assertTrue(result.ok)
        self.assertEqual(result.sql, "SELECT name FROM sales LIMIT 50")

    def test_validate_keeps_existing_limit_when_semicolon_present(self):
        result = validate_and_sanitize_sql("SELECT name FROM sales LIMIT 10;", row_limit=50)
        self.assertTrue(result.ok)
        self.assertEqual(result.sql, "SELECT name FROM sales LIMIT 10")

    def test_validate_rejects_multiple_statements(self):
        result = validate_and_sanitize_sql("SELECT name FROM sales; DROP TABLE sales", row_limit=50)
        self.assertFalse(result.ok)
        self.assertIn("single SELECT statement", result.reason)

    def test_validate_accepts_fenced_cte_query(self):
        raw = """```sql
WITH ranked AS (
    SELECT * FROM sales
)
SELECT * FROM ranked;
```"""
        result = validate_and_sanitize_sql(raw, row_limit=50)
        self.assertTrue(result.ok)
        self.assertEqual(result.sql, "WITH ranked AS ( SELECT * FROM sales ) SELECT * FROM ranked LIMIT 50")


if __name__ == "__main__":
    unittest.main()
