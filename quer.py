from flaskblog import app
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import time

serialize_ins = serializer(app.config['SECRET_KEY'], expires_in=5)


data = {'user_id': 1}

token = serialize_ins.dumps(data).decode('utf-8')
print(token)

# time.sleep(10)

try:
    value = serialize_ins.loads(token)
    print(value)
except Exception as e:
    print(f"{e}")




