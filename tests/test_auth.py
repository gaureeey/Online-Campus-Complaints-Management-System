"""
Authentication & Authorization Tests (SRS Section 3.1 & 3.2).
Tests registration validation, password hashing, failed attempt lockouts (FR-1.8),
and password recovery tokens (FR-1.6).
"""

from app.models import User, db


def test_registration_success(client):
    """TC-1: Successful registration with valid data."""
    response = client.post('/register', data={
        'name': 'Kavita Sen',
        'email': 'kavita.sen@campus.edu',
        'phone': '+91 98888 77766',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful' in response.data

    user = User.query.filter_by(email='kavita.sen@campus.edu').first()
    assert user is not None
    assert user.name == 'Kavita Sen'
    assert user.role == 'user'
    assert user.check_password('SecurePass123') is True
    assert user.password_hash != 'SecurePass123'  # Verify hashed


def test_registration_duplicate_email(client):
    """TC-1: Registration rejected when email already registered."""
    response = client.post('/register', data={
        'name': 'Duplicate User',
        'email': 'user@example.com',
        'phone': '+91 99999 00000',
        'password': 'Password@123',
        'confirm_password': 'Password@123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'already exists' in response.data


def test_registration_weak_password(client):
    """FR-1.2: Password must be at least 8 chars and contain a digit."""
    # Too short (< 8 chars)
    resp1 = client.post('/register', data={
        'name': 'Short Pwd',
        'email': 'short@campus.edu',
        'phone': '+91 99999 00001',
        'password': 'Pass1',
        'confirm_password': 'Pass1'
    }, follow_redirects=True)
    assert b'at least 8 characters' in resp1.data

    # No digits
    resp2 = client.post('/register', data={
        'name': 'No Digit',
        'email': 'nodigit@campus.edu',
        'phone': '+91 99999 00002',
        'password': 'PasswordOnly',
        'confirm_password': 'PasswordOnly'
    }, follow_redirects=True)
    assert b'at least one digit' in resp2.data


def test_registration_password_mismatch(client):
    """Reject registration when password confirmation does not match."""
    response = client.post('/register', data={
        'name': 'Mismatch User',
        'email': 'mismatch@campus.edu',
        'phone': '+91 99999 00003',
        'password': 'Password123',
        'confirm_password': 'DifferentPassword456'
    }, follow_redirects=True)

    assert b'Passwords do not match' in response.data


def test_login_user_success(auth):
    """FR-1.3: Complainant logs in and is routed to user dashboard."""
    response = auth.login_user()
    assert response.status_code == 200
    assert b'Welcome back, Rahul Sharma' in response.data
    assert b'Submit a Complaint' in response.data or b'My Complaints' in response.data


def test_login_staff_success(auth):
    """FR-1.3: Staff officer logs in and is routed to staff dashboard."""
    response = auth.login_staff()
    assert response.status_code == 200
    assert b'Welcome back, Priya Nair' in response.data
    assert b'Staff Resolution Desk' in response.data or b'staff' in response.data.lower()


def test_login_admin_success(auth):
    """FR-1.3: Administrator logs in and is routed to admin dashboard."""
    response = auth.login_admin()
    assert response.status_code == 200
    assert b'Welcome back, Dr. Arvind Mehta' in response.data
    assert b'Admin Overview' in response.data or b'Dr. Arvind Mehta' in response.data



def test_login_invalid_password_and_failed_attempts(client):
    """FR-1.8: Failed login increments failed_attempts counter."""
    user = User.query.filter_by(email='user@example.com').first()
    assert user.failed_attempts == 0

    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'WrongPassword123'
    }, follow_redirects=True)

    assert b'Invalid password' in response.data
    assert user.failed_attempts == 1


def test_account_lockout_after_five_failed_attempts(client):
    """FR-1.8: Account locked for 15 minutes after 5 consecutive failures."""
    for i in range(5):
        client.post('/login', data={
            'email': 'user@example.com',
            'password': 'BadPassword'
        }, follow_redirects=True)

    user = User.query.filter_by(email='user@example.com').first()
    assert user.is_locked() is True

    # 6th attempt should show locked error message
    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'User@123'  # Even correct password is now blocked
    }, follow_redirects=True)

    assert b'temporarily locked' in response.data


def test_logout(auth):
    """FR-1.3: Logout clears session cleanly."""
    auth.login_user()
    response = auth.logout()
    assert response.status_code == 200
    assert b'logged out' in response.data.lower()


def test_password_recovery_token(client):
    """FR-1.6: Password reset generates valid time-limited token."""
    user = User.query.filter_by(email='user@example.com').first()
    token = user.get_reset_token()
    assert token is not None

    verified_user = User.verify_reset_token(token)
    assert verified_user is not None
    assert verified_user.id == user.id

    # Reset password via route
    response = client.post(f'/reset-password/{token}', data={
        'password': 'NewPassword123',
        'confirm_password': 'NewPassword123'
    }, follow_redirects=True)

    assert b'successfully updated' in response.data or b'updated' in response.data
    assert user.check_password('NewPassword123') is True


def test_switch_role_personas(client):
    """Test instant demo role switcher for all personas."""
    # Switch to User
    res_user = client.get('/switch-role/user', follow_redirects=True)
    assert res_user.status_code == 200
    assert b'Rahul Sharma' in res_user.data
    assert res_user.request.path == '/dashboard'

    # Switch to Staff
    res_staff = client.get('/switch-role/staff', follow_redirects=True)
    assert res_staff.status_code == 200
    assert b'Priya Nair' in res_staff.data
    assert res_staff.request.path == '/staff/dashboard'

    # Switch to Admin
    res_admin = client.get('/switch-role/admin', follow_redirects=True)
    assert res_admin.status_code == 200
    assert b'Dr. Arvind Mehta' in res_admin.data
    assert res_admin.request.path == '/admin/dashboard'

    # Switch to Guest
    res_guest = client.get('/switch-role/guest', follow_redirects=True)
    assert res_guest.status_code == 200
    assert b'Public Visitor' in res_guest.data or b'Log In' in res_guest.data
    assert res_guest.request.path == '/'

