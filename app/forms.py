"""
Flask-WTF Form Definitions with CSRF Protection and Field Validations.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField,
    BooleanField, IntegerField, SubmitField, HiddenField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError,
    Optional, NumberRange
)
from app.models import User


class LoginForm(FlaskForm):
    """User / Staff / Admin login form."""
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Citizen registration form with duplicate check and password strength (FR-1.1, FR-1.2)."""
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=7, max=20, message="Enter a valid phone number.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        """Reject duplicate emails (FR-1.2)."""
        existing = User.query.filter_by(email=email.data.strip().lower()).first()
        if existing:
            raise ValidationError("An account with this email address already exists.")

    def validate_password(self, password):
        """Ensure password contains at least one digit (FR-1.2)."""
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password must contain at least one digit.")


class ForgotPasswordForm(FlaskForm):
    """Password reset request form."""
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    """Password reset completion form."""
    password = PasswordField('New Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Update Password')

    def validate_password(self, password):
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password must contain at least one digit.")


class ComplaintForm(FlaskForm):
    """Grievance submission form with file upload support (FR-2.1, FR-2.3)."""
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired(message="Please select a category.")
    ])
    subject = StringField('Complaint Subject', validators=[
        DataRequired(message="Subject is required."),
        Length(min=5, max=200, message="Subject must be between 5 and 200 characters.")
    ])
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent')
    ], default='Medium')
    location = StringField('Location / Room / Area', validators=[
        Optional(),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message="Please describe the issue in detail."),
        Length(min=10, max=4000, message="Description must be at least 10 characters.")
    ])
    attachment = FileField('Attachment (JPG, PNG, PDF max 5 MB)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Images (JPG, PNG) and PDF documents only.')
    ])
    is_anonymous = BooleanField('File Anonymously')
    submit = SubmitField('Submit Grievance')


class CommentForm(FlaskForm):
    """Conversation thread reply form (FR-2.8)."""
    message = TextAreaField('Message', validators=[
        DataRequired(message="Message cannot be empty."),
        Length(min=2, max=2000)
    ])
    submit = SubmitField('Send Message')


class FeedbackForm(FlaskForm):
    """Star rating and review form (FR-6.1)."""
    rating = IntegerField('Rating', validators=[
        DataRequired(message="Please select a star rating from 1 to 5."),
        NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
    ])
    comments = TextAreaField('Feedback Remarks', validators=[
        Optional(),
        Length(max=1000)
    ])
    submit = SubmitField('Submit Feedback')


class StatusUpdateForm(FlaskForm):
    """Status change and assignment update form."""
    status = SelectField('Status', choices=[
        ('Submitted', 'Submitted'),
        ('Assigned', 'Assigned / Under Review'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed')
    ])
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent')
    ])
    staff_id = SelectField('Assign Technician', coerce=int, validators=[Optional()])
    admin_remark = TextAreaField('Remarks / Action Taken', validators=[Optional()])
    rejection_reason = TextAreaField('Rejection Reason (Mandatory if Rejecting)', validators=[Optional()])
    submit = SubmitField('Save Updates')


class CategoryForm(FlaskForm):
    """Category CRUD form (FR-3.4)."""
    name = StringField('Category Name', validators=[
        DataRequired(message="Category name is required."),
        Length(min=2, max=100)
    ])
    description = TextAreaField('Description', validators=[Optional()])
    sla_hours = IntegerField('Target SLA (Hours)', default=48, validators=[
        DataRequired(),
        NumberRange(min=1, max=720, message="SLA must be between 1 and 720 hours.")
    ])
    icon = StringField('Bootstrap Icon Class', default='bi-tag', validators=[Optional()])
    default_priority = SelectField('Default Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent')
    ], default='Medium')
    submit = SubmitField('Save Category')


class ProfileForm(FlaskForm):
    """Profile update form (FR-1.5)."""
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=100)
    ])
    phone = StringField('Phone', validators=[
        Optional(),
        Length(max=20)
    ])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Profile')


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Current password is required.")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="New password is required."),
        Length(min=8, message="New password must be at least 8 characters.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password."),
        EqualTo('new_password', message="Passwords must match.")
    ])
    submit = SubmitField('Change Password')

    def validate_new_password(self, field):
        if not any(char.isdigit() for char in field.data):
            raise ValidationError("New password must contain at least one digit.")
