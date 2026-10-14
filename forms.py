"""
Re-export WTForms from app.forms for root convenience.
"""

from app.forms import (
    LoginForm,
    RegistrationForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ComplaintForm,
    CommentForm,
    FeedbackForm,
    StatusUpdateForm,
    CategoryForm,
    ProfileForm,
    ChangePasswordForm
)

__all__ = [
    'LoginForm',
    'RegistrationForm',
    'ForgotPasswordForm',
    'ResetPasswordForm',
    'ComplaintForm',
    'CommentForm',
    'FeedbackForm',
    'StatusUpdateForm',
    'CategoryForm',
    'ProfileForm',
    'ChangePasswordForm'
]
