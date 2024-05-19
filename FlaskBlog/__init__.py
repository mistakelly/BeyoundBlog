from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import LoginManager
from flask_mail import Mail
import os
from flaskblog.config import Config


# flask initialization
app = Flask(__name__)
app.config.from_object(Config)

# initiailize mail instance.
mail = Mail(app)

# initialize bcrypt config (for pasword hashing)
bcrypt = Bcrypt(app)

# flask login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from flaskblog import routes