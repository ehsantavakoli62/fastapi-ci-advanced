# models.py

import sqlite3
from typing import List, Dict, Any, Optional

DB_NAME = 'practise_rest.db'

def get_db_connection() -> sqlite3.Connection:
    """Returns a database connection (بازگرداندن اتصال دیتابیس)"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# --- Author CRUD ---

def create_author(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    # استفاده از کوئری پارامتری
    cursor.execute(
        """
        INSERT INTO Author (first_name, last_name, middle_name)
        VALUES (?, ?, ?)
        """,
        (data.get('first_name'), data.get('last_name'), data.get('middle_name', None))
    )
    conn.commit()
    author_id = cursor.lastrowid
    conn.close()
    return author_id

def get_author_by_id(author_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Author WHERE id = ?", (author_id,))
    author = cursor.fetchone()
    conn.close()
    return dict(author) if author else None

def get_books_by_author_id(author_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE author_id = ?", (author_id,))
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def delete_author(author_id: int) -> bool:
    """Deletes an author (triggers CASCADE deletion of books) (وظیفه ۳)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Author WHERE id = ?", (author_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Book CRUD ---

def create_book(data: Dict[str, Any]) -> Optional[int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Book (book_name, publish_year, ISBN, author_id)
            VALUES (?, ?, ?, ?)
            """,
            (data.get('book_name'), data.get('publish_year'), data.get('ISBN'), data.get('author_id'))
        )
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return book_id
    except sqlite3.IntegrityError:
        # ISBN constraint violation
        conn.close()
        return None 

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

def update_book(book_id: int, data: Dict[str, Any], partial: bool = False) -> bool:
    """Handles PUT (partial=False) and PATCH (partial=True) updates (وظیفه ۲)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    set_clauses = []
    params = []
        
    for key, value in data.items():
        if key in ['book_name', 'publish_year', 'ISBN', 'author_id']:
            set_clauses.append(f"{key} = ?")
            params.append(value)
    
    if not set_clauses:
        conn.close()
        return False # Nothing to update
        
    params.append(book_id)
    
    query = f"UPDATE Book SET {', '.join(set_clauses)} WHERE id = ?"
    
    try:
        cursor.execute(query, tuple(params))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated
    except sqlite3.IntegrityError:
        conn.close()
        return False # ISBN violation

def delete_book(book_id: int) -> bool:
    """Deletes a book by ID (وظیفه ۲)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Book WHERE id = ?", (book_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
