import os
import sqlite3
from contextlib import contextmanager

from config import DB_PATH
from document_parser import extract_doc_id


@contextmanager
def get_connection(db_path = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path = DB_PATH):
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS search_results (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                processed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                publication_date TEXT,
                content_type TEXT,
                pdf_url TEXT NOT NULL UNIQUE,
                body TEXT
            )
        """)
        conn.commit()


def drop_db(db_path = DB_PATH):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Dropped '{db_path}'")


def save_results(records, db_path = DB_PATH):
    """records: list of dicts like {"title": ..., "link": ...}"""
    with get_connection(db_path) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO search_results (id, title, link) VALUES (?, ?, ?)",
            [(extract_doc_id(r["link"]), r["title"], r["link"]) for r in records],
        )
        conn.commit()
        print(f"Saved {len(records)} records to '{db_path}'")


def save_documents(documents, db_path = DB_PATH):
    """documents: list of Document dataclass instances"""
    with get_connection(db_path) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO raw_documents (id, title, publication_date, content_type, pdf_url, body) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [(d.id, d.title, d.publication_date, d.content_type, d.pdf_url, d.body) for d in documents],
        )
        conn.commit()
        print(f"Saved {len(documents)} documents to '{db_path}'")
