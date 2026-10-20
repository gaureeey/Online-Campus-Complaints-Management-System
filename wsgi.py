"""
WSGI entry point for production deployment on Render, Gunicorn, etc.
Conforms to IEEE Std 830-1998 SRS.
"""

import os
from app import create_app
from app.models import db, User

config_mode = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(config_mode)

with app.app_context():
    # Ensure database tables exist
    db.create_all()
    # Auto-seed database if empty (ensures default accounts and categories exist)
    try:
        if User.query.first() is None:
            from seed import seed_database
            seed_database(app)
    except Exception as e:
        app.logger.warning(f"Production WSGI database initialization: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
