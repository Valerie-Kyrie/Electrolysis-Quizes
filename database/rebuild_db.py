# rebuild_db.py
# This script creates a clean copy of the database by copying all data from the old database to a new one.
# This corrects any schema issues and ensures all data is properly migrated and maintains sequential IDs.

import sqlite3
from pathlib import Path

OLD_DB = Path("../data/electrolysis.db")
NEW_DB = Path("../data/electrolysis_clean.db")


def get_conn(path):
    return sqlite3.connect(path)


def rebuild():
    if NEW_DB.exists():
        NEW_DB.unlink()

    old = get_conn(OLD_DB)
    new = get_conn(NEW_DB)

    old_cur = old.cursor()
    new_cur = new.cursor()

    # -------------------------
    # CREATE TABLES (same schema)
    # -------------------------
    new_cur.executescript("""
        CREATE TABLE chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_number INTEGER NOT NULL,
            title TEXT NOT NULL
        );

        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            page_number INTEGER,
            question_type TEXT NOT NULL,
            explanation TEXT,
            FOREIGN KEY(chapter_id) REFERENCES chapters(id)
        );

        CREATE TABLE answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        );
    """)

    # -------------------------
    # COPY CHAPTERS
    # -------------------------
    old_cur.execute("SELECT id, chapter_number, title FROM chapters")
    chapters = old_cur.fetchall()

    chapter_map = {}

    for old_id, num, title in chapters:
        new_cur.execute("""
            INSERT INTO chapters (chapter_number, title)
            VALUES (?, ?)
        """, (num, title))

        chapter_map[old_id] = new_cur.lastrowid

    # -------------------------
    # COPY QUESTIONS
    # -------------------------
    old_cur.execute("""
        SELECT id, chapter_id, question_text, page_number, question_type, explanation
        FROM questions
    """)
    questions = old_cur.fetchall()

    question_map = {}

    for q in questions:
        old_id, chapter_id, text, page, qtype, explanation = q

        new_chapter_id = chapter_map[chapter_id]

        new_cur.execute("""
            INSERT INTO questions (
                chapter_id,
                question_text,
                page_number,
                question_type,
                explanation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (new_chapter_id, text, page, qtype, explanation))

        question_map[old_id] = new_cur.lastrowid

    # -------------------------
    # COPY ANSWERS
    # -------------------------
    old_cur.execute("""
        SELECT id, question_id, answer_text, is_correct
        FROM answers
    """)
    answers = old_cur.fetchall()

    for a in answers:
        _, question_id, text, correct = a

        new_question_id = question_map[question_id]

        new_cur.execute("""
            INSERT INTO answers (
                question_id,
                answer_text,
                is_correct
            )
            VALUES (?, ?, ?)
        """, (new_question_id, text, correct))

    new.commit()
    old.close()
    new.close()

    print("✅ Database rebuilt successfully → electrolysis_clean.db")


if __name__ == "__main__":
    rebuild()