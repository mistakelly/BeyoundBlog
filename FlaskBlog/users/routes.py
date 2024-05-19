from flask import Blueprint, redirect, flash, url_for, render_template, session, request, current_app
from flask_login import current_user, logout_user, login_user, login_required
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from flaskblog.users.forms import (
    Register_Form,
    Login_Form,
    Update_Account_Form,
    Reset_Request_Form,
    Reset_Password,
)
from flaskblog.users.utils import send_email
from flaskblog.models import User
from flaskblog import bcrypt, db


users = Blueprint("users", __name__)


# User Registration route
@users.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect("index_page")

    form = Register_Form()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash(f"Account Created for {form.username.data}", "success")

        return redirect(url_for("users.login_page"))
    return render_template("register.html", form=form)


# User Login Route
@users.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect("index_page")
    """
    Get users email from form email field
    Check if  email exists in database
    if email exists:
        User has account in our database
        Unhash the password of the user
        Compare the the unhashed password with the form password.
        if Match:
            Login the User in, add remember me field.
    """
    form = Login_Form()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # log the user in using session object from flask
            login_user(user, remember=form.remember_me.data)

            next = session.pop("next", None)

            flash(
                f"Success! You're logged in and ready to go, {user.username}", "success"
            )

            return redirect(next) if next else redirect(url_for("main.index_page"))

        else:
            flash("Login Unsuccessful. Please Check email or password", "error")

    # save the next parameter in session.
    next_page = request.args.get("next")
    session["next"] = next_page

    return render_template("login.html", form=form)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account_page():
    form = Update_Account_Form()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        # update profile pic.
        if form.profile_pic.data:
            profile_pic_filname = secure_filename(form.profile_pic.data.filename)

            _, file_ext = os.path.splitext(profile_pic_filname)

            random_filename = f"{uuid4()}{file_ext}"

            profile_pic_ = os.path.join(current_app.config["UPLOAD_FOLDER"], random_filename)
            form.profile_pic.data.save(profile_pic_)
            current_user.image_file = random_filename
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"An error occured {e}")
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for("static", filename="profile_pics/" + "default.jpg")
    return render_template("account.html", form=form, img_file=img_file)


# logout route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index_page"))


# Send TOTP for reseting email.
@users.route("/password/reset/", methods=["GET", "POST"])
def send_email_link():
    form = Reset_Request_Form()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(email=form.email.data).first()
            print(user)
            if user:
                # try:
                send_email(user)

                flash(
                    "Email sent successfully!, follow link to reset your password",
                    category="success",
                )
                # except Exception as e:
                # flash(f"Failed to send email: {e}", category="error")

                return redirect(url_for("users.send_email_link"))
            else:
                flash("Email does not exist in our system", category="error")

    return render_template("reset_email.html", form=form)


# Password Reset
@users.route("/password/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = Reset_Password()
    user = User.validate_token(token, expire_sec=300)

    if request.method == "POST" and form.validate_on_submit():
        # user variable would be None if the time set on the link expires.
        if user is None:
            flash(
                "Error: The provided token is either invalid or has expired",
                category="error",
            )
            return redirect(url_for("users.send_email_link"))

        #  hash user password
        user.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        db.session.commit()
        flash(
            "Your password has been successfully reset. You can now log in with your new password.",
            category="success",
        )

        # redirect user to login page
        return redirect(url_for("users.login_page"))

    # render reset password template on GET REQUEST.
    return render_template(
        "reset_password.html",
        form=form,
        legend_title="Reset your password",
        title="Password reset",
    )
