from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from mysql.connector import Error
import logging
import cloudinary
import cloudinary.uploader

# Import configuration and database modules
from config import (
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    DEBUG,
    configure_cloudinary,
    CLOUD_UPLOAD_FOLDER,
)
from database import get_db_connection, close_connection, test_connection, init_connection_pool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
configure_cloudinary()

# Flask configuration
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database connection pool
init_connection_pool()

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Public pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-story')
def add_story_page():
    return render_template('add_story.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# Test database connection route (for debugging)
@app.route('/api/test-db', methods=['GET'])
def test_db():
    """Test database connection - useful for debugging."""
    success, message = test_connection()
    if success:
        return jsonify({'status': 'success', 'message': message}), 200
    else:
        return jsonify({'status': 'error', 'message': message}), 500

# Get all stories
@app.route('/api/stories', methods=['GET'])
def get_stories():
    connection = get_db_connection()
    if not connection:
        success, message = test_connection()
        return jsonify({'error': f'Database connection failed. {message}'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stories ORDER BY created_at DESC")
        stories = cursor.fetchall()
        
        # Convert datetime to string
        for story in stories:
            if story['created_at']:
                story['created_at'] = story['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        close_connection(connection)
        return jsonify(stories), 200
    except Error as e:
        logger.error(f"Error fetching stories: {e}")
        close_connection(connection)
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Add new story
@app.route('/api/stories', methods=['POST'])
def add_story():
    connection = get_db_connection()
    if not connection:
        success, message = test_connection()
        logger.error(f"Database connection failed: {message}")
        return jsonify({'error': f'Database connection failed. {message}'}), 500
    
    try:
        author_name = request.form.get('author_name', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        content = request.form.get('content', '').strip()
        
        if not all([author_name, title, description, content]):
            close_connection(connection)
            return jsonify({'error': 'All fields are required'}), 400
        
        photo_url = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                if not allowed_file(file.filename):
                    close_connection(connection)
                    return jsonify({'error': 'Invalid image format'}), 400
                try:
                    upload_result = cloudinary.uploader.upload(
                        file,
                        folder=CLOUD_UPLOAD_FOLDER,
                        resource_type='image'
                    )
                    photo_url = upload_result.get('secure_url')
                    logger.info("Photo uploaded to Cloudinary: %s", photo_url)
                except Exception as upload_error:
                    logger.error("Cloudinary upload failed: %s", upload_error)
                    close_connection(connection)
                    return jsonify({'error': 'Image upload failed'}), 500
        
        cursor = connection.cursor()
        query = """INSERT INTO stories (author_name, title, description, content, photo_url) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (author_name, title, description, content, photo_url))
        connection.commit()
        
        story_id = cursor.lastrowid
        cursor.close()
        close_connection(connection)
        
        logger.info(f"Story added successfully with ID: {story_id}")
        return jsonify({'message': 'Story added successfully', 'id': story_id}), 201
    except Error as e:
        logger.error(f"Error adding story: {e}")
        close_connection(connection)
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error adding story: {e}")
        close_connection(connection)
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# Delete story (admin only)
@app.route('/api/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    username = request.headers.get('X-Admin-Username')
    password = request.headers.get('X-Admin-Password')
    
    if not username or not password:
        return jsonify({'error': 'Admin credentials required'}), 401
    
    connection = get_db_connection()
    if not connection:
        success, message = test_connection()
        return jsonify({'error': f'Database connection failed. {message}'}), 500
    
    try:
        # Verify admin credentials
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", 
                      (username, password))
        admin = cursor.fetchone()
        
        if not admin:
            cursor.close()
            close_connection(connection)
            return jsonify({'error': 'Invalid admin credentials'}), 401
        
        # Ensure story exists before deleting
        cursor.execute("SELECT id FROM stories WHERE id = %s", (story_id,))
        story = cursor.fetchone()
        
        if not story:
            cursor.close()
            close_connection(connection)
            return jsonify({'error': 'Story not found'}), 404
        
        # Delete story
        cursor.execute("DELETE FROM stories WHERE id = %s", (story_id,))
        connection.commit()
        
        cursor.close()
        close_connection(connection)
        
        logger.info(f"Story {story_id} deleted successfully")
        return jsonify({'message': 'Story deleted successfully'}), 200
    except Error as e:
        logger.error(f"Error deleting story: {e}")
        close_connection(connection)
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Verify admin credentials
@app.route('/api/admin/verify', methods=['POST'])
def verify_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    connection = get_db_connection()
    if not connection:
        success, message = test_connection()
        return jsonify({'error': f'Database connection failed. {message}'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", 
                      (username, password))
        admin = cursor.fetchone()
        
        cursor.close()
        close_connection(connection)
        
        if admin:
            return jsonify({'valid': True}), 200
        else:
            return jsonify({'valid': False}), 401
    except Error as e:
        logger.error(f"Error verifying admin: {e}")
        close_connection(connection)
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    # Test database connection on startup
    logger.info("Testing database connection...")
    success, message = test_connection()
    if success:
        logger.info(f"✓ {message}")
    else:
        logger.warning(f"⚠ {message}")
        logger.warning("The application will start, but database operations may fail.")
        logger.warning("Please check your database configuration in config.py")
    
    app.run(debug=DEBUG, port=5000, host='0.0.0.0')