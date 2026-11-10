"""
Layer 1: SQL Injection Armor (Deep Query Inspector)
Wraps database drivers (sqlite3, psycopg2, pymysql, duckdb) to detect and neutralize
unparameterized SQL injection patterns, stacked queries, tautologies, and time-based blind SQLi.
"""

import re
import sys

SQL_INJECTION_PATTERN = re.compile(
    r"(\bUNION\s+(ALL\s+)?SELECT\b|"
    r"\b(DROP|TRUNCATE)\s+TABLE\b|"
    r"\bALTER\s+TABLE\b|"
    r"'\s*OR\s*['\d\w]+=['\d\w]+|"
    r"\"\s*OR\s*[\"\d\w]+=[\"\d\w]+|"
    r"\bOR\s+(1\s*=\s*1|true\b)|"
    r"--\s*($|\w)|"
    r"/\*.*?\*/|"
    r"';\s*(DROP|DELETE|TRUNCATE|SHUTDOWN|UPDATE)\b|"
    r";\s*(DROP|TRUNCATE)\s+TABLE\b|"
    r"\b(WAITFOR\s+DELAY|pg_sleep\s*\(|sleep\s*\(|benchmark\s*\()|"
    r"\b(information_schema\.(tables|columns)|sqlite_master\b))",
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
    """Wraps database Cursor to intercept execute/executemany."""
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
    """Wraps database Connection to return ArmoredCursorProxy."""
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
    # 1. Hook sqlite3.connect
    try:
        import sqlite3
        orig_connect = sqlite3.connect

        def armored_connect(*args, **kwargs):
            conn = orig_connect(*args, **kwargs)
            return ArmoredConnectionProxy(conn, core)

        sqlite3.connect = armored_connect
    except ImportError:
        pass

    # 2. Hook psycopg2 if present
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

    # 3. Hook pymysql if present
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
