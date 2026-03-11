import sqlite3
from datetime import datetime

DB_NAME = "debugger_logs.db"

def init_db():
    """
    Creates the database and table if not exists
    Run this once at app startup
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debug_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            broken_code TEXT NOT NULL,
            error_msg   TEXT NOT NULL,
            fixed_code  TEXT,
            status      TEXT,
            time_taken  REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready!")


def save_log(broken_code, error_msg, fixed_code, status, time_taken):
    """
    Saves every debug session to database
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO debug_logs
        (timestamp, broken_code, error_msg, fixed_code, status, time_taken)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        broken_code,
        error_msg,
        fixed_code,
        status,
        time_taken
    ))

    conn.commit()
    conn.close()


def get_all_logs():
    """
    Returns all past debug sessions
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, error_msg, status, time_taken
        FROM debug_logs
        ORDER BY id DESC
        LIMIT 20
    """)

    logs = cursor.fetchall()
    conn.close()
    return logs


def get_stats():
    """
    Returns total sessions, success rate, avg time
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM debug_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM debug_logs WHERE status='success'")
    success = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(time_taken) FROM debug_logs")
    avg_time = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total": total,
        "success": success,
        "failed": total - success,
        "success_rate": f"{(success/total*100):.1f}%" if total > 0 else "0%",
        "avg_time": f"{avg_time:.1f}s"
    }


def clear_history():
    """
    Clears all past debug sessions
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debug_logs")
    conn.commit()
    conn.close()


# Test database
if __name__ == "__main__":
    init_db()
    save_log(
        broken_code="print(undefined_var)",
        error_msg="NameError: undefined_var",
        fixed_code="undefined_var = 'hello'\\nprint(undefined_var)",
        status="success",
        time_taken=4.2
    )
    print("Logs:", get_all_logs())
    print("Stats:", get_stats())
