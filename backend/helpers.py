from tables import *
from sqlalchemy import and_
from sqlalchemy.sql import func
import datetime as dt
import uuid
import redis

loginTokens = {}
cacheTokens = redis.Redis()


def authenticateAPI(token):
        try:
            keys = cacheTokens.keys('*')
            for key in keys:
                print(f"Accepted token: {token}")
                print(f"Curent decoding: {cacheTokens.get(key).decode()} of type {type(cacheTokens.get(key).decode())}")
                if cacheTokens.get(key).decode() == str(token):
                    print("Auth DONE!!!")
                    return True
                
            return False

            # if token in loginTokens.values():
            #     return True
            # else:
            #     return False

        except Exception as e:
            return {"error":str(e)}

def getLoginToken(enteredUsername, enteredPassword):
    try:
        data={"login":None,"token":None,"user_display_name":None,"store_display_name":None,"errorMessage":None}
        loginCredentials = {
            "U":"U", 
            "Harsh":"harsh",
            "rebel1": "rebel1"
            }
       
        
        print("LoginCreds so far: ", loginCredentials)
        if enteredUsername in loginCredentials:
            if loginCredentials[enteredUsername] == enteredPassword:
                data['login'] = "authenticated"
                data['user_display_name'] = str(enteredUsername)
                token = str(uuid.uuid4())
                # loginTokens[enteredUsername] = token
                ttl = dt.timedelta(seconds=86400)           #86400 seconds in a day (to set to expire at the end of the day)
                cacheTokens.setex(enteredUsername, ttl,  value = token)
                data['token'] = token
            else:
                data['login'] = "not_authenticated"
                data['errorMessage'] = "Username and/or Password is Incorrect"                
        else:
            data['login'] = "not_authenticated"
            data['errorMessage'] = "Username and/or Password is Incorrect"
        return data
        
    except Exception as e:
        return {"error":str(e)}


def getSumMetrics(geoFilter="",brandFilter=0,dateFilter="",geoId=0):
    try:
        session=Session()
        passFilters=[]
        failFilters=[]
        passFilters.append(getattr(Logs,"passed")==1)
        failFilters.append(getattr(Logs,"failed")==1)
        if geoFilter != "" and geoId != 0:
            passFilters.append(getattr(Logs,geoFilter)==geoId)
            failFilters.append(getattr(Logs,geoFilter)==geoId)
        if brandFilter != 0:
            passFilters.append(getattr(Logs,'brand')==brandFilter)
            failFilters.append(getattr(Logs,'brand')==brandFilter)
        if dateFilter != "":
            dates = getDateFilters(dateFilter)
            passFilters.extend(dates)
            failFilters.extend(dates)
        passed=session.query(Logs.S_No).filter(and_(*passFilters)).count()
        failed=session.query(Logs.S_No).filter(and_(*failFilters)).count()
        total=passed+failed
        res = {"total":total,"passed":passed,"failed":failed,"passpercent":getPercent(passed/total),"failpercent":getPercent(failed/total)}
        session.close()
        return res
    
    except Exception as e:
        return {"error":str(e)}

def getPercent(num):
    return "{:.0%}".format(num)

def fetchZonesBrands():
    try:
        session=Session()
        data={"zones":[],"brands":[]}

        # Query zones
        zones = session.query(Zone).all()
        for instance in zones:
            d={"id":instance.id, "name":instance.name}
            data["zones"].append(d)
        
        # Query brands
        brands = session.query(Brand).all()
        for instance in brands:
            d={"id":instance.id, "name":instance.name}
            data["brands"].append(d)

        data["metrics"]=getMetrics(dateFilter="day")
        data["graphData"]=graphData(dateFilter="day")
        # data["graphData"]=graphDataTemp()
        session.close()

        return data

    except Exception as e:
        return {"error":str(e)}

def getDateFilters(dateFilter):
    dates=[]
    #currDate = dt.date.today()
    currDate = dt.date(2020,3,15)
    if dateFilter == "day":
        dates.append(getattr(Logs,'date') == currDate)

    elif dateFilter == "month":
        dates.append(getattr(Logs,'month_no') == currDate.month)
        dates.append(getattr(Logs,'year') == currDate.year)

    elif dateFilter == "week":
        dates.append(getattr(Logs,'week_no')==currDate.isocalendar()[1])

    elif dateFilter == "year":
        dates.append(getattr(Logs,'year') == currDate.year)
    
    return dates


def graphDataTemp():
    try:
        intervalMins = 15
        #passedData = [0 for i in range (0, int(1440/intervalMins)+1)]
        #failedData = [0 for i in range (0, int(1440/intervalMins)+1)]
        passedData = [0 for i in range(0,24)]
        failedData = [0 for i in range(0,24)]
        labels = []
        for i in range(0, 24):
            labels.append(str(i)+":00")
        session = Session()

        for i in range (0, int(1440/intervalMins)+1):
            q = session.query(Logs).filter(Logs.interval == i)
            if not q.all():
                print("Skipping ", i)
                continue
            print("Result at:", i)
            result = q[0].__dict__
            passedData.append(result["passedQC"])
            failedData.append(result["failedQC"])
            hour = int(i/4)
            minute = (i-(4*hour))*15
            labels.append(str(hour)+":"+str(minute))

        session.close()
        res = {"labels":labels,"passed":passedData, "failed": failedData}
        return res

    except Exception as e:
        return {"error1":str(e)}


def graphData(geoFilter="",brandFilter=0,dateFilter="",geoId=0):
    try:
        # passedData=[0 for i in range(0,14)]
        # failedData=[0 for i in range(0,14)]
        passedData = [0 for i in range(0,24)]
        failedData = [0 for i in range(0,24)]
        labels = []
        for i in range(0, 24):
            labels.append(str(i)+":00")
            
        session=Session()

        filters=[]

        if geoFilter != "" and geoId != 0:
            filters.append(getattr(Logs,geoFilter)==geoId)
        if brandFilter != 0:
            filters.append(getattr(Logs,'brand')==brandFilter)
        if dateFilter != "":
            dateFilterList = getDateFilters(dateFilter)
            filters.extend(dateFilterList)
        q=session.query(Logs.interval,func.sum(Logs.passed).label('passed'),func.sum(Logs.failed).label('failed')).filter(and_(*filters)).group_by(Logs.interval/4)
        ctr=0
        arr=0
        for i in q.all():
            ctr+=1
            print("Q: ", i)
            passedData[arr]+=i.passed
            failedData[arr]+=i.failed
            if ctr%4==0:
                arr+=1
        print("Passed: ", passedData)
        print("Failed: ", failedData)
        session.close()
        res = {"labels": labels, "passed":passedData,"failed":failedData}
        return res
    except Exception as e:
        return {"error":str(e)}

def getMetrics(geoFilter="",brandFilter=0,dateFilter="",geoId=0):
    try:
        session=Session()
        passFilters=[]
        failFilters=[]
        passFilters.append(getattr(Logs,"passed")==1)
        failFilters.append(getattr(Logs,"failed")==1)
        if geoFilter != "" and geoId != 0:
            passFilters.append(getattr(Logs,geoFilter)==geoId)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
            failFilters.append(getattr(Logs,geoFilter)==geoId)
        if brandFilter != 0:
            passFilters.append(getattr(Logs,'brand')==brandFilter)
            failFilters.append(getattr(Logs,'brand')==brandFilter)
        if dateFilter != "":
            dates = getDateFilters(dateFilter)
            passFilters.extend(dates)
            failFilters.extend(dates)
        passed=session.query(Logs.S_No).filter(and_(*passFilters)).count()
        failed=session.query(Logs.S_No).filter(and_(*failFilters)).count()
        total=passed+failed
        if total == 0:
            res = {"total":total,"passed":passed,"failed":failed,"passpercent":0,"failpercent":0}
            session.close()
            return res
        res = {"total":total,"passed":passed,"failed":failed,"passpercent":getPercent(passed/total),"failpercent":getPercent(failed/total)}
        session.close()
        return res
    
    except Exception as e:
        return {"error":str(e)}


def fetchList(geoFilter,brandFilter,dateFilter,id):
    try:
        session=Session()
        data={"data":[]}

        if geoFilter == "country":
            zones = session.query(Zone).all()
            for instance in zones:
                d={"id":instance.id, "name":instance.name}
                data["data"].append(d)

        elif geoFilter == "zone":
            states = session.query(State).filter(State.zone==id).all()
            for zone in states:
                d={"id":zone.id, "name":zone.name}
                data["data"].append(d)
        
        elif geoFilter == "state":
            cities = session.query(City).filter(City.state==id).all()
            for city in cities:
                d={"id":city.id, "name":city.name}
                data["data"].append(d)

        elif geoFilter == "city":
            stores = session.query(Store).filter(Store.city==id).all()
            for store in stores:
                d={"id":store.id, "name":store.name,"clientId":store.client_id,"address":store.address}
                data["data "].append(d)

        elif geoFilter == "store":
            machines = session.query(Machine).filter(Machine.store==id).all()
            for machine in machines:
                d={"id":machine.id, "mac":machine.mac,"serialNumber":machine.serial_number,"modelNumber":machine.model_number,"manufacturedOn":machine.manufactured_on,"installedOn":machine.installed_on,"warrantyExpiresOn":machine.warranty_expires_on,"softwareVersion":machine.software_version}
                data["data"].append(d)

        data["metrics"]=getMetrics(geoFilter,brandFilter,dateFilter,id)
        data["graphData"]=graphData(geoFilter,brandFilter,dateFilter,id)
        # data["graphData"]=graphDataTemp()
        session.close()
        return data

    except Exception as e:
        return {"error":str(e)}
