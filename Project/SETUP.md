# Blog Writing Website - Setup Guide

## Quick Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Using MySQL Command Line
```bash
mysql -u root -p < database_setup.sql
```

#### Option B: Manual Setup
1. Open MySQL and create the database:
```sql
CREATE DATABASE blog_website;
```

2. Run the SQL commands from `database_setup.sql` in your MySQL client.

### 3. Configure Database Connection

Edit `config.py` and update the database credentials:

```python
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL host
    'port': 3306,              # MySQL port (default: 3306)
    'user': 'root',            # Your MySQL username
    'password': 'Sid@12345',    # Your MySQL password
    'database': 'blog_website', # Database name
    ...
}
```

### 4. Test Database Connection

Start the Flask app:
```bash
python app.py
```

The app will automatically test the database connection on startup. Check the console for connection status.

You can also test the connection via API:
```bash
curl http://localhost:5000/api/test-db
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Troubleshooting Database Connection Issues

### Error: "Database connection failed"

1. **Check MySQL is running:**
   ```bash
   # Windows
   net start MySQL
   
   # Linux/Mac
   sudo systemctl status mysql
   ```

2. **Verify database exists:**
   ```sql
   SHOW DATABASES;
   ```
   Make sure `blog_website` is listed.

3. **Check credentials in config.py:**
   - Verify username and password are correct
   - Test connection manually:
   ```bash
   mysql -u root -p
   ```

4. **Check if tables exist:**
   ```sql
   USE blog_website;
   SHOW TABLES;
   ```
   You should see `stories` and `admin_users` tables.

5. **Check MySQL port:**
   - Default is 3306
   - If using a different port, update `config.py`

6. **Firewall issues:**
   - Make sure MySQL port (3306) is not blocked

### Common Issues

- **"Access denied"**: Wrong username/password
- **"Can't connect"**: MySQL server not running or wrong host/port
- **"Database doesn't exist"**: Run `database_setup.sql` first
- **"Table doesn't exist"**: Run `database_setup.sql` to create tables

## Default Admin Credentials

After running `database_setup.sql`:
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT:** Change these credentials after first login!

## Project Structure

```
Blog Writing/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database connection handling
├── database_setup.sql     # Database schema
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html
│   ├── add_story.html
│   └── admin.html
├── static/               # Static files
│   ├── css/
│   └── js/
└── uploads/              # Uploaded images (created automatically)
```

## Environment Variables (Optional)

For production, you can override settings using environment variables:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=blog_website
export DB_PORT=3306
```

## Production Deployment

1. Set `DEBUG = False` in `config.py` or via environment variable
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper database credentials
4. Configure HTTPS
5. Set up proper file upload limits and storage

