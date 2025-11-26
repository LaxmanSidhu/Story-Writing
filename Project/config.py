"""
Configuration file for the Blog Writing application.
All database, application, and third-party settings are defined here.
"""

import logging
import os

from dotenv import load_dotenv
load_dotenv()

import cloudinary

logger = logging.getLogger(__name__)

# Database Configuration
# Override these values using environment variables for production deployment
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Sid@12345'),
    'database': os.environ.get('DB_NAME', 'blog_website'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False,
    'connect_timeout': 10,
    'raise_on_warnings': True
}

# Application Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# Cloudinary Configuration
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
CLOUD_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
CLOUD_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')
CLOUD_UPLOAD_FOLDER = os.environ.get('CLOUDINARY_UPLOAD_FOLDER', 'blog_stories')


def configure_cloudinary():
    """Configure the global Cloudinary client using environment variables."""
    missing = [var for var, value in {
        'CLOUDINARY_CLOUD_NAME': CLOUD_NAME,
        'CLOUDINARY_API_KEY': CLOUD_API_KEY,
        'CLOUDINARY_API_SECRET': CLOUD_API_SECRET,
    }.items() if not value]

    if missing:
        logger.warning(
            "Cloudinary credentials missing: %s. Image uploads will fail.",
            ", ".join(missing),
        )

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_API_KEY,
        api_secret=CLOUD_API_SECRET,
    )
