import mysql.connector
from mysql.connector import pooling

# Create a connection pool
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "ROOT",
    "database": "anemia_db",
    "auth_plugin": 'mysql_native_password'
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # Adjust based on your expected traffic
    **db_config
)

def get_connection():
    return connection_pool.get_connection()