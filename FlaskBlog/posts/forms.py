from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired


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
