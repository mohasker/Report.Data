#!/usr/bin/env python3
"""Reference numbering service (ADR-0005 rev 1, decision D-10).

One service, many configurable series. A number moves reserved -> issued, or
reserved -> cancelled. A cancelled number is never reused, so every gap in the
register is explainable rather than merely observed.

The atomic counter is modelled here with a SQLite transaction because it is the
standard-library primitive available offline. In production the same contract is
implemented with the orchestration platform's atomic data-store update. What matters
is the contract, which this module states and the tests exercise: no two concurrent
callers may ever receive the same number.
"""
import os, sqlite3, threading


class NumberingService:
    def __init__(self, db_path=":memory:"):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=MEMORY")
        self.lock = threading.Lock()
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS counters (
            series_id TEXT, year_key TEXT, scope_key TEXT, next_value INTEGER,
            PRIMARY KEY (series_id, year_key, scope_key));
        CREATE TABLE IF NOT EXISTS register (
            number_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id TEXT, year_key TEXT, scope_key TEXT, sequence_value INTEGER,
            formatted TEXT UNIQUE, state TEXT, job_id TEXT, document_id TEXT,
            reason TEXT, migrated INTEGER DEFAULT 0,
            UNIQUE (series_id, year_key, scope_key, sequence_value));
        """)
        self.db.commit()

    # -- configuration -----------------------------------------------------
    def register_series(self, series, start_number=None):
        """series: the NumberingSeries row (dict)."""
        self.series = getattr(self, "series", {})
        self.series[series["SeriesID"]] = series
        self.start = getattr(self, "start", {})
        self.start[series["SeriesID"]] = int(
            start_number if start_number is not None else series.get("StartNumber") or 1)

    def seed_manual_history(self, series_id, year_key, scope_key, last_manual_number):
        """Continue an existing manual register instead of colliding with it (D-10)."""
        with self.lock:
            self.db.execute(
                "INSERT OR REPLACE INTO counters VALUES (?,?,?,?)",
                (series_id, year_key, scope_key, int(last_manual_number) + 1))
            self.db.commit()

    # -- lifecycle ---------------------------------------------------------
    def reserve(self, series_id, year_key, scope_key, job_id):
        s = self.series[series_id]
        with self.lock:
            cur = self.db.cursor()
            cur.execute("BEGIN IMMEDIATE")
            cur.execute("SELECT next_value FROM counters WHERE series_id=? AND year_key=? "
                        "AND scope_key=?", (series_id, year_key, scope_key))
            row = cur.fetchone()
            value = row[0] if row else self.start.get(series_id, 1)
            cur.execute("INSERT OR REPLACE INTO counters VALUES (?,?,?,?)",
                        (series_id, year_key, scope_key, value + 1))
            formatted = self.format(s, value, year_key, scope_key)
            cur.execute("INSERT INTO register (series_id, year_key, scope_key, sequence_value, "
                        "formatted, state, job_id) VALUES (?,?,?,?,?,'Reserved',?)",
                        (series_id, year_key, scope_key, value, formatted, job_id))
            number_id = cur.lastrowid
            self.db.commit()
        return {"number_id": number_id, "formatted": formatted, "sequence": value,
                "state": "Reserved"}

    def issue(self, number_id, document_id):
        with self.lock:
            cur = self.db.cursor()
            cur.execute("SELECT state FROM register WHERE number_id=?", (number_id,))
            state = cur.fetchone()[0]
            if state != "Reserved":
                raise ValueError(f"cannot issue a number in state {state}")
            cur.execute("UPDATE register SET state='Issued', document_id=? WHERE number_id=?",
                        (document_id, number_id))
            self.db.commit()

    def cancel(self, number_id, reason):
        if not reason:
            raise ValueError("a cancellation reason is mandatory: a gap must be explainable")
        with self.lock:
            cur = self.db.cursor()
            cur.execute("SELECT state FROM register WHERE number_id=?", (number_id,))
            state = cur.fetchone()[0]
            if state != "Reserved":
                raise ValueError(f"cannot cancel a number in state {state}")
            cur.execute("UPDATE register SET state='Cancelled', reason=? WHERE number_id=?",
                        (reason, number_id))
            self.db.commit()

    def reuse_attempt(self, series_id, year_key, scope_key, sequence_value, job_id):
        """Deliberately attempt silent reuse. Must fail."""
        s = self.series[series_id]
        formatted = self.format(s, sequence_value, year_key, scope_key)
        cur = self.db.cursor()
        cur.execute("INSERT INTO register (series_id, year_key, scope_key, sequence_value, "
                    "formatted, state, job_id) VALUES (?,?,?,?,?,'Reserved',?)",
                    (series_id, year_key, scope_key, sequence_value, formatted, job_id))
        self.db.commit()

    # -- formatting --------------------------------------------------------
    @staticmethod
    def format(series, value, year_key, scope_key):
        pattern = series["FormatPattern"]
        pad = int(series.get("PadWidth") or 3)
        return (pattern
                .replace("{ENTITY}", series.get("_entity_code", "AH"))
                .replace("{TYPE}", series["DocumentTypeCode"])
                .replace("{YYYY}", year_key)
                .replace("{YY}", year_key[-2:])
                .replace("{PROJECT}", scope_key if scope_key != "COMPANY" else "")
                .replace("{CLIENT}", scope_key if scope_key != "COMPANY" else "")
                .replace("{NNN}", str(value).zfill(pad)))

    def all_numbers(self):
        cur = self.db.cursor()
        cur.execute("SELECT formatted, state, reason FROM register ORDER BY number_id")
        return cur.fetchall()
