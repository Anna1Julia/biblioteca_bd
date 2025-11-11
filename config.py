import os
from pathlib import Path
import mysql.connector
from mysql.connector import pooling

_POOL = None

def _get_pool():
    global _POOL
    if _POOL is not None:
        return _POOL
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = int(os.environ.get('DB_PORT', '3306'))
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'db_atividade17')
    _POOL = pooling.MySQLConnectionPool(
        pool_name="biblioteca_pool",
        pool_size=int(os.environ.get('DB_POOL_SIZE', '5')),
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return _POOL

def get_db_connection():
    """
    Returns a pooled MySQL connection. Ensure to close() after use.
    """
    pool = _get_pool()
    return pool.get_connection()

def init_database_from_schema(schema_path: str = None):
    """
    Initialize the database executing the full SQL schema provided by the user.
    It will create the database and all required tables if they don't exist.
    """
    schema_file = schema_path or str(Path(__file__).parent / 'schema.sql')
    if not Path(schema_file).exists():
        return
    sql_text = Path(schema_file).read_text(encoding='utf-8')

    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = int(os.environ.get('DB_PORT', '3306'))
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', '')
    bootstrap_conn = mysql.connector.connect(
        host=db_host, port=db_port, user=db_user, password=db_password
    )
    try:
        try:
            bootstrap_conn.autocommit = True
        except Exception:
            pass
        cur = bootstrap_conn.cursor()
        
        for statement in [s.strip() for s in sql_text.split(';') if s.strip()]:
            cur.execute(statement)
    finally:
        bootstrap_conn.close()

