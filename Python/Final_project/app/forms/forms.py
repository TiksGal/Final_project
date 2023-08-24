from app.models.models import Player
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    name = StringField("Name", [DataRequired()])
    surname = StringField("Surname", [DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField(
        "Repeat password", [EqualTo("password", "Passwords must match")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = Player.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already in use")

    def validate_email(self, email):
        user = Player.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use")
