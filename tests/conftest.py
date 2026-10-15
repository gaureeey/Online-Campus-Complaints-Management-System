"""
pytest configuration and shared test fixtures for OCMS backend.
Configures in-memory SQLite database, test client, and seeded entities.
"""

import pytest
from app import create_app
from app.models import db, User, Category, Complaint, ComplaintUpdate, Department


@pytest.fixture(scope='function')
def app():
    """Create test application instance with in-memory database."""
    test_app = create_app('testing')
    with test_app.app_context():
        db.create_all()

        # Seed default test users
        admin = User(
            name="Dr. Arvind Mehta",
            email="admin@example.com",
            phone="+91 98111 22334",
            role="admin",
            department="Administration",
            is_active=True
        )
        admin.set_password("Admin@123")
        db.session.add(admin)

        staff = User(
            name="Priya Nair",
            email="staff@example.com",
            phone="+91 98222 33445",
            role="staff",
            department="IT & Networking",
            is_active=True
        )
        staff.set_password("Staff@123")
        db.session.add(staff)

        user1 = User(
            name="Rahul Sharma",
            email="user@example.com",
            phone="+91 98765 43210",
            role="user",
            department="Computer Science",
            is_active=True
        )
        user1.set_password("User@123")
        db.session.add(user1)

        user2 = User(
            name="Ananya Iyer",
            email="user2@example.com",
            phone="+91 98333 44556",
            role="user",
            department="Electronics",
            is_active=True
        )
        user2.set_password("User@123")
        db.session.add(user2)

        # Seed default categories
        cat1 = Category(
            name="IT & Network Infrastructure",
            description="Wi-Fi, Ethernet, lab computers",
            sla_hours=12,
            icon="bi-wifi",
            is_active=True
        )
        cat2 = Category(
            name="Hostel & Accommodation",
            description="Hostel room plumbing and furniture",
            sla_hours=24,
            icon="bi-building",
            is_active=True
        )
        cat3 = Category(
            name="Electrical & Power",
            description="Lighting and circuit breakers",
            sla_hours=8,
            icon="bi-lightning-charge",
            is_active=True
        )
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        yield test_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()


class AuthHelper:
    """Helper to simulate logins for different test personas."""
    def __init__(self, client):
        self.client = client

    def login(self, email, password):
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def login_user(self):
        return self.login('user@example.com', 'User@123')

    def login_user2(self):
        return self.login('user2@example.com', 'User@123')

    def login_staff(self):
        return self.login('staff@example.com', 'Staff@123')

    def login_admin(self):
        return self.login('admin@example.com', 'Admin@123')

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    """Provides AuthHelper fixture for easy login/logout in tests."""
    return AuthHelper(client)
