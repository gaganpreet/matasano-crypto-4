import sys
import time
import hmac
try:
    from flask import Flask, request
except ImportError:
    print('Flask not installed, exiting')
    sys.exit(0)

sleep = 0.003

def bad_compare(a, b):
    for i, j in zip(a, b):
        if i != j:
            return False
        time.sleep(sleep)
    return True

app = Flask(__name__)

@app.route("/")
def hello():
    key = 'Valar Morghulis'
    file_name = request.args.get('file')
    sig = request.args.get('signature')

    if bad_compare(hmac.hmac(key, file_name), sig):
        return 'true'
    else:
        return 'false'


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sleep = float(sys.argv[1])
        print('----------->Using %f for sleep interval' % sleep)
    else:
        print('----------->Using default value %f for sleep interval (anything less than this is the value it breaks for me)' % sleep)

    app.debug = True
    app.run()
