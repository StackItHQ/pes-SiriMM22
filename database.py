import mysql.connector
from mysql.connector import Error
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sales_tracking',
    'user': 'root',
    'password': 'Sirimm@21'
}
def get_db_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_in_db(connection, data):
    """Insert or update data in the database."""
    if not connection:
        return

    try:
        cursor = connection.cursor()
        
        # Example table and columns; adjust to match your schema
        query = """
        INSERT INTO sales (id, product_name, quantity, sale_date)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            quantity = VALUES(quantity),
            sale_date = VALUES(sale_date)
        """
        
        print("Query to be executed:", query)
        print("Data to be inserted:", data)
        
        cursor.executemany(query, data)
        connection.commit()
        print(f"Inserted/Updated {cursor.rowcount} rows.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
