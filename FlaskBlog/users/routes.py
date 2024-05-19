from flask import blueprints, redirect, flash, url_for, render_template,session, request
from flask_login import current_user,logout_user, login_user, login_required
from flaskblog.forms import Register_Form, Login_Form, Update_Account_Form
from flaskblog import bcrypt, app
from flaskblog.models import User, Post,db
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

users = blueprints('users', __name__)
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

        return redirect(url_for("login_page"))
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

            return redirect(next) if next else redirect(url_for("index_page"))

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

            profile_pic_ = os.path.join(app.config["UPLOAD_FOLDER"], random_filename)
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
    return redirect(url_for("index_page"))

