# Imports
from flask import (
    session,
    url_for,
    render_template,
    redirect,
    flash,
    get_flashed_messages,
    session,
    request,
    render_template_string,
    abort,
)
from flaskblog.forms import (
    Register_Form,
    Login_Form,
    Update_Account_Form,
    NEW_POST,
    EDIT_POST,
)
from flaskblog import bcrypt, app
from flaskblog.models import User, Post, db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from uuid import uuid4


@app.route("/")
@app.route("/home", strict_slashes=False)
def index_page():
    all_posts = Post.query.all()
    return render_template("home.html", all_posts=all_posts)


@app.route("/about", strict_slashes=False)
def about_page():
    return render_template("about.html")


# User Registration route.
@app.route("/register", strict_slashes=False, methods=["GET", "POST"])
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
@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
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


@app.route("/account", methods=["GET", "POST"])
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
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index_page"))


# # # # # # # # # # # # # # # # #
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def post():
    form = NEW_POST()
    if form.validate_on_submit():
        cleaned_content = form.content.data
        post = Post(
            title=form.title.data,
            content=cleaned_content.strip(),
            user_id=current_user.id,
            author=current_user,
        )

        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index_page", post_id=post.id))
   

    return render_template("post.html", form=form)


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = EDIT_POST()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post_id = post.id
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            cleaned_content = form.content.data
            post.content = cleaned_content.strip()
            db.session.commit()
            return redirect(url_for("index_page", post_id=post_id))
        except Exception as e:
            flash(f"An error occured {e}")

    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("edit_post.html", form=form, post_id=post_id)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)

    db.session.commit()

    return redirect(url_for("index_page"))
