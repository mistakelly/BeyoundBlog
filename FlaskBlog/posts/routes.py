from flask import Blueprint, redirect, render_template, url_for, abort, flash, request
from flaskblog.posts.forms import NEW_POST, EDIT_POST
from flaskblog.models import Post, db
from flask_login import current_user, login_required

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def post():
    form = NEW_POST()
    if form.validate_on_submit():
        cleaned_content = form.content.data
        user_post = Post(
            title=form.title.data,
            content=cleaned_content.strip(),
            user_id=current_user.id,
            author=current_user,
        )

        db.session.add(user_post)
        db.session.commit()
        return redirect(url_for("main.index_page", post_id=user_post.id))

    return render_template("post.html", form=form)


@posts.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = EDIT_POST()
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)
    post_id = user_post.id
    if form.validate_on_submit():
        try:
            user_post.title = form.title.data
            cleaned_content = form.content.data
            user_post.content = cleaned_content.strip()
            db.session.commit()
            return redirect(url_for("main.index_page", post_id=post_id))
        except Exception as e:
            flash(f"An error occurred {e}")

    if request.method == "GET":
        form.title.data = user_post.title
        form.content.data = user_post.content

    return render_template("edit_post.html", form=form, post_id=post_id)


@posts.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):

    user_post = Post.query.get_or_404(post_id)

    db.session.delete(user_post)

    db.session.commit()

    return redirect(url_for("main.index_page"))
