import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Use persistent disk for SQLite database
if os.path.exists('/data'):
    logger.info("Using persistent disk at /data")
    db_path = '/data/finance_tracker.db'
    # Ensure directory is writable
    if not os.access('/data', os.W_OK):
        logger.error("No write permission to /data directory!")
else:
    logger.info("Persistent disk not found, using local database")
    db_path = 'finance_tracker.db'

logger.info(f"Database path: {db_path}")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models import db
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import all the models and forms
from models import User, Category, Budget, Expense
from forms import LoginForm, RegistrationForm, ExpenseForm, BudgetForm, CategoryForm

# Import routes - this needs to be after all other initializations
from routes import *

# Initialize database if it doesn't exist
with app.app_context():
    logger.info("Creating database tables...")
    db.create_all()
    logger.info("Database tables created")
    
    # Check if we need to initialize with demo data
    try:
        user_count = User.query.count()
        logger.info(f"Found {user_count} users in database")
        if user_count == 0:
            logger.info("Initializing database with demo data...")
            from init_db import init_db
            init_db()
            logger.info("Demo data initialized")
    except Exception as e:
        logger.error(f"Error checking user count: {e}")
        # Force table creation again
        logger.info("Forcing table creation...")
        db.drop_all()
        db.create_all()
        logger.info("Initializing database with demo data...")
        from init_db import init_db
        init_db()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

