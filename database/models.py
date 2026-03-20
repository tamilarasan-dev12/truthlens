def create_history_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def insert_history_row(conn, text, prediction, confidence):
    conn.execute(
        """
        INSERT INTO history (text, prediction, confidence)
        VALUES (?, ?, ?)
        """,
        (text, prediction, float(confidence)),
    )


def fetch_history_rows(conn, limit=200):
    return conn.execute(
        """
        SELECT id, text, prediction, confidence, created_at
        FROM history
        ORDER BY datetime(created_at) DESC, id DESC
        LIMIT ?
        """,
        (int(limit),),
    ).fetchall()


def fetch_dashboard_metrics(conn):
    totals = conn.execute(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN prediction = 'Fake' THEN 1 ELSE 0 END) AS fake_count,
            SUM(CASE WHEN prediction = 'True' THEN 1 ELSE 0 END) AS true_count,
            AVG(confidence) AS avg_confidence
        FROM history
        """
    ).fetchone()

    total = int(totals["total"] or 0)
    fake_count = int(totals["fake_count"] or 0)
    true_count = int(totals["true_count"] or 0)
    avg_confidence = float(totals["avg_confidence"] or 0.0)

    recent_activity = conn.execute(
        """
        SELECT id, text, prediction, confidence, created_at
        FROM history
        ORDER BY datetime(created_at) DESC, id DESC
        LIMIT 8
        """
    ).fetchall()

    return {
        "total_predictions": total,
        "fake_count": fake_count,
        "true_count": true_count,
        "avg_confidence": avg_confidence,
        "fake_ratio": (fake_count / total) if total else 0.0,
        "true_ratio": (true_count / total) if total else 0.0,
        "recent_activity": recent_activity,
    }
