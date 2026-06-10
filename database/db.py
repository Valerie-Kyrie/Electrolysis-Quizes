# db.py
# This module contains all database-related functions, including connection management and CRUD operations for chapters, questions, and answers.

import sqlite3
from pathlib import Path

DB_PATH = Path("data/electrolysis.db")


# ----------------------------
# Connection helper
# ----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


# ----------------------------
# Initialize database
# ----------------------------
def initialize_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # Chapters
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_number INTEGER NOT NULL,
            title TEXT NOT NULL
        )
    """)

    # Questions (UPDATED DESIGN)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            page_number INTEGER,
            question_type TEXT NOT NULL,
            FOREIGN KEY(chapter_id) REFERENCES chapters(id)
        )
    """)

    # Answers (NEW TABLE)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Chapters (UNCHANGED)
# ----------------------------
def get_all_chapters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, chapter_number, title
        FROM chapters
        ORDER BY chapter_number
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_chapter_question_count(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE chapter_id = ?
    """, (chapter_id,))

    count = cursor.fetchone()[0]
    conn.close()
    return count


def add_chapter(chapter_number, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chapters (chapter_number, title)
        VALUES (?, ?)
    """, (chapter_number, title))

    conn.commit()
    conn.close()


def update_chapter(chapter_id, chapter_number, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE chapters
        SET chapter_number = ?, title = ?
        WHERE id = ?
    """, (chapter_number, title, chapter_id))

    conn.commit()
    conn.close()


def delete_chapter(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chapters
        WHERE id = ?
    """, (chapter_id,))

    conn.commit()
    conn.close()

def get_questions_by_chapter(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               question_text,
               page_number,
               question_type
        FROM questions
        WHERE chapter_id = ?
        ORDER BY id
    """, (chapter_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM answers
        WHERE question_id = ?
    """, (question_id,))

    cursor.execute("""
        DELETE FROM questions
        WHERE id = ?
    """, (question_id,))

    conn.commit()
    conn.close()

def get_answers_for_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               answer_text,
               is_correct
        FROM answers
        WHERE question_id = ?
    """, (question_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               chapter_id,
               question_text,
               page_number,
               question_type,
               explanation
        FROM questions
        WHERE id = ?
    """, (question_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def update_question(
    question_id,
    question_text,
    page_number,
    question_type
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE questions
        SET question_text = ?,
            page_number = ?,
            question_type = ?
        WHERE id = ?
    """, (
        question_text,
        page_number,
        question_type,
        question_id
    ))

    conn.commit()
    conn.close()


def delete_answers_for_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM answers
        WHERE question_id = ?
    """, (question_id,))

    conn.commit()
    conn.close()

def add_wrong_flag_column():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE questions
            ADD COLUMN times_wrong INTEGER DEFAULT 0
        """)
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def add_explanation_column():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE questions
            ADD COLUMN explanation TEXT
        """)
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()        

def get_all_questions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               question_text,
               page_number,
               question_type
        FROM questions
        ORDER BY id
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows