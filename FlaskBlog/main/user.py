from flask import url_for
from flask_mail import Message
from flaskblog import mail

def send_email(user):
    # construct TOTP.
    token = user.get_token()
    reset_url = url_for("reset_password", token=token, _external=True)

    msg = Message(
        "Email Reset Link", sender=os.environ.get("EMAIL_USER"), recipients=[user.email]
    )

    msg.body = f"""{reset_url}
    If you did not request this link, you can ignore this message, and your password will remain unchanged. Thank you.
    """
    mail.send(msg)