import lbcapi.lbcClient as lbc
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return lbc.main()
    else:
        return json.dumps({
            'error': "Cannot get BTC price mean"
        },
            ensure_ascii=False)
