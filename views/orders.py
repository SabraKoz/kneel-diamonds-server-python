import sqlite3
import json

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM Orders o
        """)

        query_results = cursor.fetchall()

        orders = []
        for row in query_results:
            orders.append(dict(row))

        serialized_orders = json.dumps(orders)

    return serialized_orders

def retrieve_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM Orders o
        WHERE o.id = ?
        """, (pk,))

        query_results = cursor.fetchone()

        serialized_order = json.dumps(dict(query_results))

    return serialized_order

def create_order(order_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Orders (metal_id, size_id, style_id)
            VALUES (?, ?, ?)
            """,
            (order_data['metal_id'], order_data['size_id'], order_data['style_id'])
        )

    return True if cursor.rowcount > 0 else False

def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM Orders WHERE id = ?
            """, (pk,)
        )

        number_of_rows_deleted = cursor.rowcount

    return True if number_of_rows_deleted > 0 else False