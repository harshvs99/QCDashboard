from sqlalchemy import *
import time
from tables import *
def checkTime():
    #on total data where pass==1
    session=Session()
    pt=time.time()
    x=session.query(Logs).filter(and_(Logs.passed==1)).count()
    print(time.time()-pt)
    print(x)
    session.close()

def checkTime2():
    session=Session()
    pt=time.time()
    x=session.query(func.count(Logs.S_No)).filter(and_(Logs.passed==1)).scalar()
    print(x)
    print(time.time()-pt)   
    session.close()

def checkTime3():
    session=Session()
    pt=time.time()
    x=session.query(func.count(Logs.S_No)).filter(and_(Logs.passed==1,Logs.interval.in_([45,79]))).scalar()
    print(x)
    print(time.time()-pt)
    session.close()

def checkTime4():
     session=Session()
     pt=time.time()
     x=session.query(Logs).filter(and_(Logs.passed==1,Logs.interval.in_([45,79]))).count()
     print(x)
     print(time.time()-pt)
     session.close()
