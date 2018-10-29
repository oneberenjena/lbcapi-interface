import lbcapi.lbcClient as lbcl
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return lbcl.main()
    else:
        return json.dumps({
            'error': "Cannot get BTC price mean"
        },
            ensure_ascii=False)
