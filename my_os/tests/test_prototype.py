"""Проверка прототипа StudyOS: база, системные вызовы, журнал, ядро."""
import sqlite3
import tempfile
import unittest
from pathlib import Path

import src.config as config
from src import kernel, syscalls
from src.db import init_db


class TestPrototype(unittest.TestCase):
    def setUp(self):
        self.old = config.DB_PATH
        self.tmp = Path(tempfile.mkdtemp()) / "os.sqlite"
        config.DB_PATH = self.tmp
        import src.db
        src.db.DB_PATH = self.tmp
        init_db()

    def tearDown(self):
        import src.db
        config.DB_PATH = src.db.DB_PATH = self.old

    def count(self, name):
        conn = sqlite3.connect(self.tmp)
        n = conn.execute("SELECT COUNT(*) FROM syscalls_log WHERE syscall_name=?", (name,)).fetchone()[0]
        conn.close()
        return n

    def test_four_tables(self):
        conn = sqlite3.connect(self.tmp)
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertTrue({"users", "processes", "files", "syscalls_log"} <= tables)

    def test_password_is_hashed(self):
        conn = sqlite3.connect(self.tmp)
        h = conn.execute("SELECT password_hash FROM users WHERE login='admin'").fetchone()[0]
        conn.close()
        self.assertEqual(h, kernel.hash_password("admin"))

    def test_echo_logged(self):
        self.assertEqual(syscalls.sys_echo("привет"), "привет")
        self.assertEqual(self.count("sys_echo"), 1)

    def test_get_users(self):
        self.assertIn(("admin", "admin"), syscalls.sys_get_users())
        self.assertEqual(self.count("sys_get_users"), 1)

    def test_kernel_survives_error(self):
        status, result = kernel.execute("sys_div", lambda: 1 / 0)
        self.assertTrue(status.startswith("ERROR"))
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
