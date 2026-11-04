"""
Layer 1: SQL Injection Armor
Wraps sqlite3.connect and cursor factories to detect and neutralize raw SQL injection patterns.
"""

import re
import sys

SQL_INJECTION_PATTERN = re.compile(
    r"(\bUNION\s+(ALL\s+)?SELECT\b|"
    r"\bDROP\s+TABLE\b|"
    r"\bALTER\s+TABLE\b|"
    r"'\s*OR\s*['\d\w]+=['\d\w]+|"
    r"\bOR\s+1\s*=\s*1\b|"
    r"--\s*$|"
    r"/\*.*?\*/|"
    r"';\s*SHUTDOWN\b)",
    re.IGNORECASE | re.MULTILINE
)

def inspect_query(sql: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(sql, str):
        return True
    
    clean_sql = sql.strip()
    match = SQL_INJECTION_PATTERN.search(clean_sql)
    if match:
        core.record_threat(
            rule_name="SQL Injection (SQLi)",
            reason=f"Detected malicious SQL signature: '{match.group(0)}'",
            payload=clean_sql,
            block=True
        )
        return False
    return True

class ArmoredCursorProxy:
    """Wraps C-level Cursor to intercept execute/executemany."""
    def __init__(self, original_cursor, core):
        self._cursor = original_cursor
        self._core = core

    def execute(self, sql, *args, **kwargs):
        inspect_query(sql, self._core)
        return self._cursor.execute(sql, *args, **kwargs)

    def executemany(self, sql, *args, **kwargs):
        inspect_query(sql, self._core)
        return self._cursor.executemany(sql, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._cursor, name)

    def __iter__(self):
        return iter(self._cursor)

class ArmoredConnectionProxy:
    """Wraps sqlite3.Connection to return ArmoredCursorProxy."""
    def __init__(self, original_conn, core):
        self._conn = original_conn
        self._core = core

    def cursor(self, *args, **kwargs):
        orig_cur = self._conn.cursor(*args, **kwargs)
        return ArmoredCursorProxy(orig_cur, self._core)

    def execute(self, sql, *args, **kwargs):
        inspect_query(sql, self._core)
        return self._conn.execute(sql, *args, **kwargs)

    def executemany(self, sql, *args, **kwargs):
        inspect_query(sql, self._core)
        return self._conn.executemany(sql, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._conn, name)

    def __enter__(self):
        self._conn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._conn.__exit__(exc_type, exc_val, exc_tb)

def arm_sqli(core):
    # Hook sqlite3.connect
    try:
        import sqlite3
        orig_connect = sqlite3.connect

        def armored_connect(*args, **kwargs):
            conn = orig_connect(*args, **kwargs)
            return ArmoredConnectionProxy(conn, core)

        sqlite3.connect = armored_connect
    except ImportError:
        pass

    # Hook psycopg2 if present
    if "psycopg2" in sys.modules:
        try:
            import psycopg2
            orig_psy_conn = psycopg2.connect
            def armored_psy_conn(*args, **kwargs):
                conn = orig_psy_conn(*args, **kwargs)
                return ArmoredConnectionProxy(conn, core)
            psycopg2.connect = armored_psy_conn
        except Exception:
            pass

    # Hook pymysql if present
    if "pymysql" in sys.modules:
        try:
            import pymysql
            orig_my_conn = pymysql.connect
            def armored_my_conn(*args, **kwargs):
                conn = orig_my_conn(*args, **kwargs)
                return ArmoredConnectionProxy(conn, core)
            pymysql.connect = armored_my_conn
        except Exception:
            pass
