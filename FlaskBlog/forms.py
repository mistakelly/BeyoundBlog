from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    BooleanField,
    TextAreaField,
    HiddenField
)
from flask_wtf.file import FileField, file_allowed
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    EqualTo,
    Email,
    ValidationError,
)
from flaskblog.models import User, Post, db
from flaskblog import bcrypt
from flask_login import current_user


class Register_Form(FlaskForm):
    username = StringField(
        label="Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(
                min=1, max=20, message="Username must be between and 20 characters."
            ),
            Regexp(
                "^[A-Za-z][a-zA-Z0-9_.]*$",
                0,
                "Oops! Invalid Username Your username should begin with a letter and can include only letters, numbers, dots, or underscores. Spaces are not permitted.",
            ),
        ],
        render_kw={"placeholder": "username"},
    )

    # validate if username exists in the database
    def validate_username(self, username):
        if db.session.query(User).filter_by(username=username.data).first():
            raise ValidationError(
                "Username already registered. Please choose a different one"
            )

    email = EmailField(
        label="Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(
                message="Uh-oh! Invalid Email Address Please enter a valid email address. It should follow the standard format (e.g., example@email.com)."
            ),
        ],
        render_kw={"placeholder": "Email"},
    )

    # validate if email exists in the database
    def validate_email(self, email):
        if db.session.query(User).filter_by(email=email.data).first():
            raise ValidationError("email is registered. please choose another one")

    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(message="Password is required."),
            # Regexp(
            #     "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$",
            #     message="Password must be at least 8 characters long and contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character",
            # ),
        ],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "username"},
    )
    signup = SubmitField("Sign Up")


class Login_Form(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"placeholder": "Password"},
    )

    remember_me = BooleanField("Remember me")
    login = SubmitField("login")


class Logout_Form(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"placeholder": "Password"},
    )

    logout = SubmitField("Logout")


from flask_wtf.file import FileField, FileAllowed


class Update_Account_Form(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(
                min=1, max=20, message="Username must be between 1 and 20 characters."
            ),
            Regexp(
                "^[A-Za-z][a-zA-Z0-9_.]*$",
                0,
                "Oops! Invalid Username. Your username should begin with a letter and can include only letters, numbers, dots, or underscores. Spaces are not permitted.",
            ),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address."),
        ],
    )

    profile_pic = FileField(
        "Update profile picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                message="Only jpg, jpeg, and png files are allowed.",
            )
        ],
    )

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError(
                    "Username already exists. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError(
                    "Email already registered. Please choose another one."
                )

    update = SubmitField("Update")


class NEW_POST(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(message="Post title  is required.")]
    )

    content = TextAreaField(
        "Post Content", validators=[DataRequired(message="Post Content is required.")]
    )

    post = SubmitField("post")


class EDIT_POST(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(message="Post title  is required.")]
    )

    content = TextAreaField(
        "Post Content", validators=[DataRequired(message="Post Content is required.")]
    )

    edit_post = SubmitField("update")


# reset password form
class Reset_Request_Form(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Email"},
    )

    reset_email_link = SubmitField("Confirm")


class Reset_Password(FlaskForm):
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(message="Password is required."),
            # Regexp(
            #     "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$",
            #     message="Password must be at least 8 characters long and contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character",
            # ),
        ],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "username"},
    )

    token = HiddenField()
    reset_password = SubmitField(label="reset")

