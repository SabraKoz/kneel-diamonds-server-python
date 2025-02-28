import sqlite3
import json

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            m.metal,
            m.price AS metal_price,
            s.carets,
            s.price AS size_price,
            st.style,
            st.price AS style_price
        FROM Orders o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Sizes s ON s.id = o.size_id
        JOIN Styles st ON st.id = o.style_id
        """)

        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            order = {
                'id': row['id'],
                'metal': {
                    'id': row['metal_id'],
                    'metal': row['metal'],
                    'price': row['metal_price']
                },
                'size': {
                    'id': row['size_id'],
                    'carets': row['carets'],
                    'price': row['size_price']
                },
                'style': {
                    'id': row['style_id'],
                    'style': row['style'],
                    'price': row['style_price']
                }
            }

            orders.append(order)

        serialized_orders = json.dumps(orders)

    return serialized_orders

def retrieve_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            m.metal,
            m.price AS metal_price,
            s.carets,
            s.price AS size_price,
            st.style,
            st.price AS style_price
        FROM Orders o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Sizes s ON s.id = o.size_id
        JOIN Styles st ON st.id = o.style_id
        WHERE o.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()
        
        order = {
            'id': query_results['id'],
            'metal': {
                'id': query_results['metal_id'],
                'metal': query_results['metal'],
                'price': query_results['metal_price']
            },
            'size': {
                'id': query_results['size_id'],
                'carets': query_results['carets'],
                'price': query_results['size_price']
            },
            'style': {
                'id': query_results['style_id'],
                'style': query_results['style'],
                'price': query_results['style_price']
            }
        }

        serialized_order = json.dumps(order)

    return serialized_order

def create_order(order_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Orders (metal_id, size_id, style_id)
            VALUES (?, ?, ?)
            """,
            (order_data['metal_id'], order_data['size_id'], order_data['style_id'])
        )

    return True if db_cursor.rowcount > 0 else False

def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Orders WHERE id = ?
            """, (pk,)
        )

        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False

