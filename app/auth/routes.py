"""
Authentication Blueprint Routes (SRS Section 3.1: User Management).
Implements registration, login with lockout protection (FR-1.8),
password hashing (FR-1.4), logout, and tokenized password reset (FR-1.6).
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse

from app.auth import auth_bp
from app.models import db, User
from app.forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm


def is_safe_url(target):
    """Ensure redirect URL belongs to current host to prevent open redirect vulnerabilities."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User / Staff / Admin login route.
    Enforces password verification via Werkzeug and locks out after 5 failures (FR-1.8).
    """
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'staff':
            return redirect(url_for('staff.staff_dashboard'))
        return redirect(url_for('user.user_dashboard'))

    form = LoginForm()

    # Support standard form submission or WTForms validation
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('public/login.html', is_dashboard=False, form=form)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Invalid email address or password.', 'danger')
            return render_template('public/login.html', is_dashboard=False, form=form)

        # Check account lockout (FR-1.8: 15-minute lock after 5 failures)
        if user.is_locked():
            minutes_left = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
            flash(f"Account is temporarily locked due to multiple failed login attempts. Try again in {minutes_left} minute(s).", "danger")
            return render_template('public/login.html', is_dashboard=False, form=form)

        if not user.is_active:
            flash('Your account is currently deactivated. Please contact the administrator.', 'warning')
            return render_template('public/login.html', is_dashboard=False, form=form)

        # Check password hash
        if not user.check_password(password):
            user.record_failed_login()
            db.session.commit()
            remaining = 5 - user.failed_attempts
            if remaining > 0:
                flash(f"Invalid password. {remaining} attempt(s) remaining before account lockout.", "danger")
            else:
                flash("Account has been locked for 15 minutes due to 5 failed login attempts (FR-1.8).", "danger")
            return render_template('public/login.html', is_dashboard=False, form=form)

        # Authentication succeeded
        user.reset_failed_logins()
        db.session.commit()

        login_user(user, remember=remember)
        session['role'] = user.role
        session['user_id'] = user.id
        session['user_name'] = user.name

        flash(f"Welcome back, {user.name}!", "success")

        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)

        if user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff.staff_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))

    return render_template('public/login.html', is_dashboard=False, form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Complainant / Citizen registration route (FR-1.1 & FR-1.2).
    Validates duplicate email, minimum password strength (>=8 chars, contains digit).
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.user_dashboard'))

    form = RegistrationForm()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('public/register.html', is_dashboard=False, form=form)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('public/register.html', is_dashboard=False, form=form)

        if len(password) < 8 or not any(char.isdigit() for char in password):
            flash('Password must be at least 8 characters long and contain at least one digit (FR-1.2).', 'danger')
            return render_template('public/register.html', is_dashboard=False, form=form)

        # Check duplicate email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists. Please log in or use a different email.', 'danger')
            return render_template('public/register.html', is_dashboard=False, form=form)

        # Create new user
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            role='user',
            is_active=True
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('public/register.html', is_dashboard=False, form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Password recovery route (FR-1.6).
    Generates a secure time-limited token (15 mins) and displays the reset link directly.
    """
    reset_link = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            token = user.get_reset_token()
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            print("=" * 60)
            print(f"[OCMS Password Recovery] Reset link for {email}:")
            print(reset_link)
            print("=" * 60)
            flash(f"Password reset token generated! Click the link below or proceed to update your password.", "info")
        else:
            flash(f"If an account exists for {email}, a recovery link has been prepared.", "info")

    return render_template(
        'public/forgot_password.html',
        is_dashboard=False,
        reset_link=reset_link
    )


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Token verification and password update route (FR-1.6).
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.user_dashboard'))

    user = User.verify_reset_token(token)
    if not user:
        flash('The password reset link is invalid or has expired (15-minute validity). Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if len(password) < 8 or not any(char.isdigit() for char in password):
            flash('Password must be at least 8 characters long and contain at least one digit.', 'danger')
            return render_template('public/reset_password.html', is_dashboard=False, form=form, token=token)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('public/reset_password.html', is_dashboard=False, form=form, token=token)

        user.set_password(password)
        user.reset_failed_logins()
        db.session.commit()

        flash('Your password has been successfully updated. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('public/reset_password.html', is_dashboard=False, form=form, token=token)


@auth_bp.route('/logout')
def logout():
    """Logs out authenticated session and clears session data."""
    logout_user()
    session.clear()
    flash('You have been safely logged out of your session.', 'info')
    return redirect(url_for('auth.login'))
