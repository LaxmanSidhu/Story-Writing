"""
Simple script to test database connection.
Run this before starting the main application to verify your database setup.
"""

from database import test_connection
from config import DB_CONFIG

def main():
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  Password: {'*' * len(DB_CONFIG['password'])}")
    print("\nTesting connection...\n")
    
    success, message = test_connection()
    
    if success:
        print("✓ SUCCESS!")
        print(f"  {message}")
        print("\nYou can now start the Flask application with: python app.py")
    else:
        print("✗ FAILED!")
        print(f"  {message}")
        print("\nTroubleshooting steps:")
        print("  1. Make sure MySQL is running")
        print("  2. Verify credentials in config.py")
        print("  3. Check if database exists: mysql -u root -p")
        print("  4. Run database_setup.sql to create database and tables")
        print("  5. See SETUP.md for more details")
    
    print("=" * 60)
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())

