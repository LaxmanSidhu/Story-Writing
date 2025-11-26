"""
Database connection and utility functions.
Handles MySQL connections with proper error handling and retry logic.
"""

import mysql.connector
from mysql.connector import Error, pooling
from config import DB_CONFIG
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection pool configuration
pool_config = {
    'pool_name': 'blog_pool',
    'pool_size': 5,
    'pool_reset_session': True,
    **DB_CONFIG
}

# Global connection pool
connection_pool = None

def init_connection_pool():
    """Initialize the MySQL connection pool."""
    global connection_pool
    try:
        # Remove non-pool config parameters
        pool_only_config = {k: v for k, v in pool_config.items() 
                           if k not in ['charset', 'collation', 'autocommit', 'raise_on_warnings']}
        connection_pool = pooling.MySQLConnectionPool(**pool_only_config)
        logger.info("Connection pool created successfully")
        return True
    except Error as e:
        logger.warning(f"Connection pool creation failed, will use direct connections: {e}")
        connection_pool = None
        return False
    except Exception as e:
        logger.warning(f"Unexpected error creating connection pool: {e}")
        connection_pool = None
        return False

def get_db_connection():
    """
    Get a database connection from the pool.
    Falls back to direct connection if pool is not available.
    
    Returns:
        mysql.connector.connection.MySQLConnection or None
    """
    try:
        # Try to get connection from pool
        if connection_pool:
            connection = connection_pool.get_connection()
            if connection.is_connected():
                logger.debug("Connection retrieved from pool")
                return connection
        
        # Fallback to direct connection
        logger.warning("Pool not available, using direct connection")
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info("Direct connection established")
            return connection
    except Error as e:
        logger.error(f"Error getting database connection: {e}")
        logger.error(f"Connection details: host={DB_CONFIG['host']}, user={DB_CONFIG['user']}, database={DB_CONFIG['database']}")
        return None
    
    return None

def test_connection():
    """
    Test the database connection and verify the database exists.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    connection = None
    try:
        # First, try to connect without specifying database
        test_config = DB_CONFIG.copy()
        test_config.pop('database', None)
        connection = mysql.connector.connect(**test_config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES LIKE %s", (DB_CONFIG['database'],))
            db_exists = cursor.fetchone()
            
            if not db_exists:
                cursor.close()
                connection.close()
                return False, f"Database '{DB_CONFIG['database']}' does not exist. Please run database_setup.sql first."
            
            # Try to use the database
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES LIKE 'stories'")
            stories_table = cursor.fetchone()
            
            cursor.execute("SHOW TABLES LIKE 'admin_users'")
            admin_table = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not stories_table or not admin_table:
                return False, "Required tables are missing. Please run database_setup.sql to create them."
            
            return True, "Database connection successful!"
            
    except Error as e:
        error_msg = str(e)
        if connection:
            connection.close()
        
        # Provide helpful error messages
        if "Access denied" in error_msg:
            return False, f"Access denied. Please check your username and password. Error: {error_msg}"
        elif "Can't connect" in error_msg:
            return False, f"Cannot connect to MySQL server at {DB_CONFIG['host']}:{DB_CONFIG['port']}. Make sure MySQL is running. Error: {error_msg}"
        else:
            return False, f"Database connection error: {error_msg}"
    
    return False, "Unknown error occurred while testing connection"

def close_connection(connection):
    """Safely close a database connection."""
    if connection and connection.is_connected():
        try:
            connection.close()
            logger.debug("Connection closed")
        except Error as e:
            logger.error(f"Error closing connection: {e}")

