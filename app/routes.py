# -*- coding: utf-8 -*-

import json

from flask import request

from app import app
from monopoly.engine import check_for_app


@app.route("/check", methods=['GET'])
def check():
    amount = request.args.get('amount', default=1000, type=int)
    resp = check_for_app(amount)
    resp['定投额度'] = amount
    return json.dumps(resp)
