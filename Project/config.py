"""
Configuration for Flask + MySQL + Cloudinary.
Works both on local (with .env) and Railway (with env variables).
"""

import os
from dotenv import load_dotenv

# Load .env ONLY during local development.
# Railway does NOT use .env so no conflict.
load_dotenv()

import cloudinary
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# DATABASE CONFIG (Local + Railway)
# -----------------------------

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

# -----------------------------
# CLOUDINARY CONFIG
# -----------------------------

CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUD_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUD_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
CLOUD_UPLOAD_FOLDER = os.environ.get('CLOUDINARY_UPLOAD_FOLDER', 'blog_stories')

def configure_cloudinary():
    missing = []
    if not CLOUD_NAME: missing.append("CLOUDINARY_CLOUD_NAME")
    if not CLOUD_API_KEY: missing.append("CLOUDINARY_API_KEY")
    if not CLOUD_API_SECRET: missing.append("CLOUDINARY_API_SECRET")

    if missing:
        logger.warning(f"Missing Cloudinary variables: {', '.join(missing)}")

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_API_KEY,
        api_secret=CLOUD_API_SECRET
    )

# -----------------------------
# FLASK CONFIG
# -----------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "local-dev-key")
DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
