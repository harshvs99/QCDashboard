from flask import Flask, request,Response, jsonify
from flask_cors import CORS, cross_origin
from tables import *
import datetime
import redis
import json
from sqlalchemy import and_,desc
import uuid,hashlib
import time
from decimal import Decimal
import json
import TotalSQCSystems

from helpers import fetchZonesBrands,fetchList, getLoginToken, authenticateAPI

cache=redis.Redis()

app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']='Content-Type'

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)



@app.route('/getTotalSQCSystems', methods=['GET'])
@cross_origin()
def getTotalSQCSystems():
    try:
        print("Auth at: ",authenticateAPI(request.args.get('token')))
        if not authenticateAPI(request.args.get('token')):
            return json.dumps({"errorMessage": "api_auth_invalid"})

        print("for total QC systems")
        res = json.loads(cache.get("Dash-SQC-Stations-Map"))
        return json.dumps(res)
    except Exception as e:
        print(str(e))

@app.route('/showLiveStatus', methods=['GET'])
@cross_origin()
def showLive():
    if not authenticateAPI(request.args.get('token')):
        return json.dumps({"errorMessage": "api_auth_invalid"})
        
    sqc_stations_map = json.loads(cache.get("Dash-SQC-Stations-Map"))
    if request.args.get('zone') not in sqc_stations_map:
        return json.dumps({"errorMessage": "Selected Zone doesn't exists"})
    if request.args.get('state') not in sqc_stations_map[request.args.get('zone')]:
        return json.dumps({"errorMessage": "Selected State doesn't exists"})
    if request.args.get('city') not in sqc_stations_map[request.args.get('zone')][request.args.get('state')]:
        return json.dumps({"errorMessage": "Selected City doesn't exists"})
    if request.args.get('store') not in sqc_stations_map[request.args.get('zone')][request.args.get('state')][
        request.args.get('city')]:
        return json.dumps({"errorMessage": "Selected Store doesn't exists"})
    try:
        if int(request.args.get('machine')) not in \
                sqc_stations_map[request.args.get('zone')][request.args.get('state')][request.args.get('city')][
                    request.args.get('store')]:
            return json.dumps({"errorMessage": "Selected machine doesn't exists"})
    except Exception as e:
        return json.dumps({"errorMessage": "Selected machine doesn't exists"})
    session = Session()
    today_midnight_time = datetime.datetime.combine(datetime.date.today(),
                                                    datetime.time(0, 0, 0))  # +datetime.timedelta(minutes=330)
    liveDetails = session.query(Live).filter(
        and_(Live.machine == int(request.args.get('machine')), Live.updatedAt > today_midnight_time)).first()

    foodBoxLabelDum = "None"        #Dummy value, to be replace later with image recognition work
    if liveDetails is None:
        res = {"errorMessage": "Selected System is not activated today"}
    else:
        current_date = (datetime.datetime.utcnow() + datetime.timedelta(minutes=330)).strftime("%m/%d/%Y")
        res = {"current_date": current_date, "live_temp": liveDetails.live_temp, "live_weight": liveDetails.live_weight,
               "TempSensor": liveDetails.TempSensor, "weighingScale": liveDetails.weighingScale,
               "faceCamera": liveDetails.faceCamera, "foodCamera": liveDetails.foodCamera,
               "message": "not_updated"}
        if request.args.get('lastQcAt') == (liveDetails.lastQcAt + datetime.timedelta(minutes=330)).strftime(
                "%H:%M:%S"):
            session.close()
            return json.dumps(res)
        if liveDetails.lastQcAt < today_midnight_time:
            res.update({"message": "machine_inactive"})
            #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if liveDetails.lastQcAt > today_midnight_time:
            res.update({"message": "updated"})
            res.update({"lastQcAt": (liveDetails.lastQcAt + datetime.timedelta(minutes=330)).strftime("%H:%M:%S"),
                        "orderId": liveDetails.orderId,
                        "productName": liveDetails.productName, "isVeg": liveDetails.isVeg,
                        "MinWeight": liveDetails.MinWeight, "Weight": liveDetails.Weight, "MaxWeight": liveDetails.MaxWeight,
                        "weightCheckRequired": liveDetails.weightCheckRequired,
                        "MinTemp": liveDetails.MinTemp, "Temp": liveDetails.Temp, "MaxTemp": liveDetails.MaxTemp,
                        "tempCheckRequired": liveDetails.tempCheckRequired, "faceImage": liveDetails.faceImage,
                        #"FaceLabel": liveDetails.faceLabel,
                        "foodImage": liveDetails.foodImage, "FoodLabel": foodBoxLabelDum,
                        "QC_Result": liveDetails.QC_Result})
            if res['weightCheckRequired']:
                res.update({'weightInRange': False})
                if res['MinWeight'] <= res['Weight'] <= res['MaxWeight']:
                    res['weightInRange'] = True
            if res['tempCheckRequired']:
                res.update({'tempInRange': False})
                if res['MinTemp'] <= res['Temp'] <= res['MaxTemp']:
                    res['tempInRange'] = True
            try:
                passed_qcs = session.query(Orders).filter(
                    and_(Orders.machine == int(request.args.get('machine')), Orders.passed == 1)).count()
                failed_qcs = session.query(Orders).filter(
                    and_(Orders.machine == int(request.args.get('machine')), Orders.failed == 1)).count()
                total_qcs = passed_qcs + failed_qcs
                res.update({'passed_qcs': passed_qcs, 'failed_qcs': failed_qcs, 'total_qcs': total_qcs,
                            'pass_percentage': ((passed_qcs / total_qcs) * 100)})
            except:
                res.update({'passed_qcs': 0, 'failed_qcs': 0, 'total_qcs': 0, 'pass_percentage': 0})
    
    session.close()
    return json.dumps(res)

@app.route('/login', methods=['GET'])
@cross_origin()
def login():
    data={"login":None,"token":None,"user_display_name":None,"store_display_name":None,"errorMessage":None}
    #print(request.args.get('user'))
    #print(request.args.get('password'))
    enteredUsername = request.args.get('user')
    enteredPassword = request.args.get('password')
    print(f"user: {enteredUsername} and password: {enteredPassword}")
    if enteredUsername is None:
        return Response('Incomplete Info (Username missing)',500)
    elif enteredPassword is None:
        return Response('Incomplete Info (Password missing)',500)

    data = getLoginToken(enteredUsername, enteredPassword)
    if 'error' in data:
            return jsonify(data),400

    # data = resToken
    
        
    # if ((request.args.get('user') == "U")and(request.args.get('password')== "U")):
    #     data['login']="authenticated"
    #     data['token']="hjagsgakcakcdk"
    #     data['user_display_name']="Rahul"
    #     data["store_display_name"]="Mumbai"
    # else:
    #     data['login']="not_authenticated"
    
    return json.dumps(data)


@app.route('/data',methods=['GET','POST'])
@cross_origin()
def dataRouter():
    if request.method=='GET':
        if not authenticateAPI(request.args.get('token')):
            print("Data API auth not taken")
            return json.dumps({"errorMessage": "api_auth_invalid"})
        
        res = fetchZonesBrands()
        if 'error' in res:
            return jsonify(res),400
        else:
            return json.dumps(res,cls=CustomJsonEncoder)

    elif request.method=='POST':
        print(request.json)
        try:
            req = request.get_json()
            print("Request to POST:", req)
            print("Required token: ", request.json['token'])
            if not authenticateAPI(request.json['token']):
                print("Data API 2 auth not taken")
                return json.dumps({"errorMessage": "api_auth_invalid"})

            if 'geoFilter' not in req:
                return jsonify({"error":"geoFilter required"})
            if 'brandFilter' not in req:
                return jsonify({"error":"brandFilter required"})
            if 'dateFilter' not in req:
                return jsonify({"error":"dateFilter required"})
            if 'geoId' not in req:
                return jsonify({"error":"id required"})
            print(req['brandFilter'])
            res = fetchList(req['geoFilter'],req['brandFilter'],req['dateFilter'],req['geoId'])

            return json.dumps(res,cls=CustomJsonEncoder)

        except Exception as e:
            print(str(e))
            return jsonify({"error":str(e)}),400

    else:
        errMsg=f"Method {request.method} not allowed"
        return jsonify({"error":errMsg}),400


if __name__=="__main__":
    app.run(debug=True,port=6003)




