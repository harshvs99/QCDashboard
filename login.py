from flask import Flask, request,Response, jsonify
from flask_cors import CORS, cross_origin
import redis
import json
from sqlalchemy import and_,desc
import uuid,hashlib
import time
from decimal import Decimal
import json

from helpers import fetchZonesBrands,fetchList

cache=redis.Redis()

app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']='Content-Type'

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)



@app.route('/login',methods=['GET','POST'])
@cross_origin()
def dataRouter():

    if request.method=='GET':
        

        res = fetchZonesBrands()

        if 'error' in res:
            return jsonify(res),400
        else:
            return json.dumps(res,cls=CustomJsonEncoder)

    elif request.method=='POST':
        try:
            req = request.get_json()

            if 'geoFilter' not in req:
                return jsonify({"error":"geoFilter required"})
            if 'brandFilter' not in req:
                return jsonify({"error":"brandFilter required"})
            if 'dateFilter' not in req:
                return jsonify({"error":"dateFilter required"})
            if 'geoId' not in req:
                return jsonify({"error":"id required"})

            res = fetchList(req['geoFilter'],req['brandFilter'],req['dateFilter'],req['geoId'])

            return json.dumps(res,cls=CustomJsonEncoder)

        except Exception as e:

            return jsonify({"error":str(e)}),400

    else:
        errMsg=f"Method {request.method} not allowed"
        return jsonify({"error":errMsg}),400


if __name__=="__main__":
    app.run(debug=True,port=6003)




