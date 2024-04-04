from PyQt6.QtSql import QSqlQuery

def create_table(db):
    query = QSqlQuery(db)
    query.exec("""
        CREATE TABLE IF NOT EXISTS popular_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            popular_name TEXT,
            cite TEXT,
            short_title TEXT,
            final INTEGER DEFAULT 0
        )
    """)

def insert_data(db, data):
    query = QSqlQuery(db)
    query.prepare("""
        INSERT INTO popular_names (popular_name, cite, short_title)
        VALUES (:popular_name, :cite, :short_title)
    """)
    query.bindValue(":popular_name", data['popular_name'])
    query.bindValue(":cite", data['cite'])
    query.bindValue(":short_title", data['short_title'])
    query.exec()

def update_data(db, row_id, column, value):
    query = QSqlQuery(db)
    query.prepare(f"UPDATE popular_names SET {column} = :value WHERE id = :id")
    query.bindValue(":value", value)
    query.bindValue(":id", row_id)
    query.exec()