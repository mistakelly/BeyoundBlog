from flask import Blueprint, request, render_template
from flaskblog.models import Post, db

main = Blueprint('main', __name__)

@main.route("/", methods=['POST', 'GET'])
@main.route("/home", strict_slashes=False, methods=['GET', 'POST'])
def index_page():
    print("inside the index_page")
    page = request.args.get("page", type=int)
    all_posts = (
        db.session.query(Post)
        .order_by(Post.id.desc())
        .paginate(page=page, per_page=4, error_out=False)
    )

    return render_template("home.html", all_posts=all_posts)


@main.route("/about", strict_slashes=False)
def about_page():
    return render_template("about.html")
