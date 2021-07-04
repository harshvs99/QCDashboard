import time
from tables import *
from sqlalchemy import and_

def check():
    session=Session()
    t=time.time()
    passed = session.query(Logs).filter(and_(Logs.zone==2,Logs.passed==1)).count()
    failed = session.query(Logs).filter(and_(Logs.zone==2,Logs.failed==1)).count()
    print(time.time()-t)
    print(f"passed:{passed},failed:{failed}")
check()
