import os
class Config:
    SECRET_KEY = os.environ.get('FLASKBLOG_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKBLOG_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    UPLOAD_FOLDER = (os.environ.get('FLASKBLOG_PROFILE_PATH'))
