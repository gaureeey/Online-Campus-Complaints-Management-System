"""
Application Factory for Online Complaint Management System (OCMS).
Configures database, login manager, CSRF protection, blueprints, and error handlers.
"""

import os
from datetime import datetime
from flask import Flask, render_template, session, url_for as flask_url_for, request, redirect, flash
from flask_login import LoginManager, current_user, login_user
from flask_wtf.csrf import CSRFProtect

from config import config
from app.models import db, User, Category, Notification

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user retrieval callback."""
    return db.session.get(User, int(user_id))


def smart_url_for(endpoint, **values):
    """
    Intelligent url_for resolution that gracefully supports both root-level
    names (e.g. 'login', 'my_complaints') and blueprint-prefixed names
    (e.g. 'auth.login', 'user.my_complaints').
    """
    try:
        return flask_url_for(endpoint, **values)
    except Exception:
        for prefix in ['auth', 'user', 'admin', 'staff', 'main']:
            try:
                return flask_url_for(f"{prefix}.{endpoint}", **values)
            except Exception:
                pass
        # Fallback to standard url_for to raise clear exception if not found
        return flask_url_for(endpoint, **values)


def create_app(config_name='default'):
    """App Factory pattern creating configured Flask instance."""
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    )

    app_config = config.get(config_name, config['default'])
    app.config.from_object(app_config)

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Inject smart url_for into Jinja2 templates
    app.jinja_env.globals['url_for'] = smart_url_for

    # Global Context Processor
    @app.context_processor
    def inject_global_template_vars():
        active_role = None
        unread_count = 0
        if current_user.is_authenticated:
            active_role = current_user.role
            try:
                unread_count = Notification.query.filter_by(
                    user_id=current_user.id,
                    is_read=False
                ).count()
            except Exception:
                unread_count = 0
        else:
            active_role = session.get('role', None)

        try:
            active_categories = Category.query.filter_by(is_active=True).all()
        except Exception:
            active_categories = []

        return {
            'current_year': datetime.utcnow().year,
            'active_role': active_role,
            'categories': active_categories,
            'unread_notifications_count': unread_count
        }

    # Demo Quick Persona Switcher (For Evaluation and Viva Presentations)
    @app.route('/switch-role/<role>')
    def switch_role(role):
        """
        Quick demo login switcher:
        - guest: logs out
        - user: signs in Rahul Sharma (Complainant)
        - staff: signs in Priya Nair (Staff Officer)
        - admin: signs in Dr. Arvind Mehta (Administrator)
        """
        if role == 'guest':
            session.clear()
            from flask_login import logout_user
            logout_user()
            flash('Switched to Guest (Public Visitor) view.', 'info')
            return redirect(url_for('main.index'))
        
        target_email = {
            'user': 'user@example.com',
            'staff': 'staff@example.com',
            'admin': 'admin@example.com'
        }.get(role)

        if target_email:
            demo_user = User.query.filter_by(email=target_email).first()
            if not demo_user:
                # Fallback to any user with that role
                demo_user = User.query.filter_by(role=role).first()
            
            if demo_user:
                login_user(demo_user)
                session['role'] = demo_user.role
                session['user_id'] = demo_user.id
                session['user_name'] = demo_user.name
                flash(f"Switched persona to: {demo_user.name} ({demo_user.role.title()}).", "success")

                if demo_user.role == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
                elif demo_user.role == 'staff':
                    return redirect(url_for('staff.staff_dashboard'))
                else:
                    return redirect(url_for('user.user_dashboard'))

        flash(f"Role '{role}' not recognized or no demo user found in database.", "warning")
        return redirect(url_for('main.index'))

    # Custom Error Handlers (SRS NFR-4)
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html', is_dashboard=False), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html', is_dashboard=False), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html', is_dashboard=False), 500

    # Register Blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.user.routes import user_bp
    from app.staff.routes import staff_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    return app
