from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import NumberRange
from app.models import User, Boardgame


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email adress.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username")


class PostForm(FlaskForm):
    post = TextAreaField(
        "Say something", validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField("Submit")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")


class AddBoardgame(FlaskForm):
    title = TextAreaField(
        "Boardgame Title", validators=[DataRequired(), Length(min=1, max=140)]
    )
    player_number_min = IntegerField(
        "Min players", validators=[DataRequired(), NumberRange(min=1, max=None)]
    )
    player_number_max = IntegerField(
        "Max players", validators=[DataRequired(), NumberRange(min=1, max=None)]
    )
    playtime_low = IntegerField(
        "Min Time in minute", validators=[DataRequired(), NumberRange(min=0, max=None)]
    )
    playtime_max = IntegerField(
        "Max Time in minute", validators=[DataRequired(), NumberRange(min=0, max=None)]
    )
    genre = TextAreaField("Genre", validators=[DataRequired(), Length(min=1, max=140)])

    difficulty = SelectField(
        "Difficulty",
        choices=[("", "Not Selected"), ('Easy', 'Easy'),
                 ('Medium', 'Medium'), ('Hard', 'Hard')],
        id="difficulty"
    )

    submit = SubmitField("Add")


class RandomGame(FlaskForm):
    player_number = IntegerField(
        "Players number", validators=[NumberRange(min=0, max=None)], id="player_number"
    )
    genre = TextAreaField("Genre",
                          validators=[Length(min=0, max=140)],
                          id="genre")

    difficulty = SelectField(
        "Difficulty",
        choices=[("", "Not Selected"), ('Easy', 'Easy'),
                 ('Medium', 'Medium'), ('Hard', 'Hard')],
        id="difficulty"
    )

    time = IntegerField("Time", validators=[NumberRange(min=1, max=None)], id="time")
