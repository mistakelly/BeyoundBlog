from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import LoginManager

# flask initialization
app = Flask(__name__)

# sqlalchemy config
app.config["SECRET_KEY"] = "x9c5K\x1c\xf7\x0e\xf7\xa2Wy\x94o\xe4(\xd11"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:31006569@localhost/FlaskBlog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
import os
# bcrypt config (for pasword hashing)
bcrypt = Bcrypt(app)

# flask login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
app.config["UPLOAD_FOLDER"] = (
    "/Users/mistarkelly/vagrant_project/My-Projects/Python_dir/Everything_python/FlaskBlog/flaskblog/static/profile_pics"
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from flaskblog import routes

