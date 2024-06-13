from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Form to register a user"""

    username = StringField('Username', validators=[InputRequired()])

    password = PasswordField("Password", validators=[InputRequired()])

    email = StringField('Email', validators=[InputRequired()])

    first_name = StringField('First Name', validators=[InputRequired()])

    last_name = StringField('Last Name', validators=[InputRequired()])

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Form to login a user"""

    username = StringField('Username', validators=[InputRequired()])

    password = PasswordField("Password", validators=[InputRequired()])

    submit = SubmitField("Login")


class FeedbackForm(FlaskForm):
    """Form to add Feedback"""

    title = StringField('Title', validators=[InputRequired(), Length(max=100)])

    content = StringField('Content', validators=[InputRequired()])
