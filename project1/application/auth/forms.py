from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(message=("Username required"))])
    password = PasswordField(label="Password", validators=[
        DataRequired(message=("Password required"))])
    confirm = PasswordField(label="Password confirmation", validators=[
        DataRequired(message=("Password confirmation required")), EqualTo(
            "password", message=("Passwords do not match"))])


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(message=("Username required"))])
    password = PasswordField(label="Password", validators=[
        DataRequired(message=("Password required"))])