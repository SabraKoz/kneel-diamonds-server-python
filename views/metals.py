import sqlite3
import json

def get_all_metals():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        """)

        query_results = db_cursor.fetchall()

        metals = []
        for row in query_results:
            metals.append(dict(row))

        serialized_metals = json.dumps(metals)

    return serialized_metals

def retrieve_metal(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        WHERE m.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()

        serialized_metal = json.dumps(dict(query_results))

    return serialized_metal

def update_metal(id, metal_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
        WHERE id = ?
        """,
        (metal_data['metal'], metal_data['price'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False