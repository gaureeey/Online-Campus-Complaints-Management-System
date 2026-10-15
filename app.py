"""
Online Complaint Management System (OCMS) - Root Entry Point
Executes the Flask application using the application factory.
Conforms to IEEE Std 830-1998 SRS.
"""

import os
from app import create_app
from app.models import db

config_mode = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_mode)

with app.app_context():
    # Ensure database tables exist
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    print(f" * Starting OCMS on http://127.0.0.1:{port} (Debug: {debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
