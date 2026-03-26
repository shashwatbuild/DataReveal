import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import backend.api as api


class BackendSqlFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.sqlite_dir = Path(self.tmpdir.name)
        self.dataset_id = "sql_case"
        db_path = self.sqlite_dir / f"{self.dataset_id}.db"

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE t_sales (name TEXT, age INTEGER)")
        cur.executemany(
            "INSERT INTO t_sales (name, age) VALUES (?, ?)",
            [("Alice", 30), ("Bob", 25)],
        )
        conn.commit()
        conn.close()

        self.original_sqlite_dir = api.SQLITE_DIR
        self.original_generate_sql = api.generate_sql
        self.original_generate_answer_sql = api.generate_answer_sql

        api.SQLITE_DIR = self.sqlite_dir
        api.generate_answer_sql = lambda **kwargs: "ok"

    def tearDown(self):
        api.SQLITE_DIR = self.original_sqlite_dir
        api.generate_sql = self.original_generate_sql
        api.generate_answer_sql = self.original_generate_answer_sql
        self.tmpdir.cleanup()

    def test_backend_ask_accepts_query_with_trailing_semicolon(self):
        api.generate_sql = lambda **kwargs: "SELECT name, age FROM t_sales;"
        client = TestClient(api.app)

        response = client.post(
            "/ask",
            json={"query": "show rows", "dataset_id": self.dataset_id, "mode": "sql", "top_k": 4},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["mode_used"], "sql")
        self.assertEqual(payload["sql"], "SELECT name, age FROM t_sales LIMIT 50")
        self.assertEqual(len(payload["result_preview"]["rows_preview"]), 2)

    def test_backend_ask_accepts_multiline_query_without_limit(self):
        api.generate_sql = lambda **kwargs: """SELECT
name,
age
FROM t_sales
ORDER BY age DESC
"""
        client = TestClient(api.app)

        response = client.post(
            "/ask",
            json={"query": "show rows", "dataset_id": self.dataset_id, "mode": "sql", "top_k": 4},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["sql"], "SELECT name, age FROM t_sales ORDER BY age DESC LIMIT 50")
        self.assertEqual(payload["result_preview"]["rows_preview"][0]["name"], "Alice")


if __name__ == "__main__":
    unittest.main()
