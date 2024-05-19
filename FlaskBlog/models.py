from itsdangerous import URLSafeTimedSerializer as serializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from flaskblog import app, login_manager
from flask_login import LoginManager, UserMixin


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

@login_manager.user_loader
def load_user(user_id :str):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, autoincrement=True, unique=True
    )
    username: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(
        db.String(50), nullable=False, default='default.jpg'
    )
    password: Mapped[str] = mapped_column(db.String(60), nullable=False)
    # relationship with post
    # post: Mapped[Base] = mapped_column(db.relationship("Post", backref="author", lazy=True))
    posts = db.relationship("Post", backref="author", lazy=True)

    def get_token(self):
        serialize = serializer(app.config['SECRET_KEY'])

        data = {'user_id': self.id}

        return serialize.dumps(data)
    
    @staticmethod
    def validate_token(token, expire_sec=30):
        serialize = serializer(app.config['SECRET_KEY'])

        try:
            user_id = serialize.loads(token, max_age=expire_sec)['user_id']
        except Exception as e:
            return None
        return User.query.get(user_id)
        # return db.session.query(User).filter_by(id=confirm_token['user_id'])






    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}') {self.content} "

with app.app_context():
    db.create_all()

