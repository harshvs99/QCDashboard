from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary,TIMESTAMP
import datetime
engine=create_engine('mysql+mysqlconnector://root:root@localhost:3306/kms')
Base=declarative_base()
Session=sessionmaker()
Session.configure(bind=engine)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key= True)
    username = Column(String(50))
    password = Column(String(50))
    client_id = Column(String(50))
    display_name = Column(String(50))
    is_active = Column()
    email = Column(String(100))
    contact = Column(String(50))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class Summary(Base):
    __tablename__ = 'summary'
    interval = Column(Integer, primary_key = True)
    passedQC = Column(Integer)
    failedQC = Column(Integer)

class Zone(Base):
    __tablename__="zone"
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    State=relationship("State")
    Logs=relationship("Logs")

class State(Base):
    __tablename__="state"
    id=Column(Integer,primary_key=True)
    zone=Column(Integer,ForeignKey('zone.id'))
    name=Column(String(50))
    Zone=relationship("Zone",back_populates="State")
    City=relationship("City")
    Logs=relationship("Logs")

class City(Base):
    __tablename__="city"
    id=Column(Integer,primary_key=True)
    state=Column(Integer,ForeignKey('state.id'))
    name=Column(String(50))
    State=relationship("State",back_populates="City")
    Logs=relationship("Logs")
    Store=relationship("Store")

class Store(Base):
    __tablename__="store"
    id=Column(Integer,primary_key=True)
    city=Column(Integer,ForeignKey('city.id'))
    client_id=Column(String(100))
    name=Column(String(100))
    City=relationship("City",back_populates="Store")
    address=Column(String(100))
    created_at=Column(TIMESTAMP)
    updated_at=Column(TIMESTAMP)
    Machine=relationship("Machine")
    Logs=relationship("Logs")

class Machine(Base):
    __tablename__="machine"
    id=Column(Integer,primary_key=True)
    store=Column(Integer,ForeignKey('store.id'))
    Store=relationship("Store",back_populates="Machine")
    mac=Column(String(17))
    serial_number=Column(String(25))
    model_number=Column(String(25))
    manufactured_on=Column(TIMESTAMP)
    installed_on=Column(TIMESTAMP)
    warranty_expires_on=Column(TIMESTAMP)
    software_version=Column(String(25))

class Brand(Base):
    __tablename__="brand"
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    Logs=relationship("Logs")
    

class Live(Base):
    __tablename__ = 'live'
    mac = Column(String, nullable=False,primary_key=True)
    machine = Column(Integer,nullable=False)
    user = Column(Integer,nullable=False)
    updatedAt = Column(TIMESTAMP, nullable = False, default = datetime.datetime.utcnow())
    lastQcAt = Column(TIMESTAMP)
    orderId = Column(String)
    productName = Column(String)
    isVeg = Column(String)
    MinWeight = Column(String)
    Weight = Column(String)
    MaxWeight = Column(String)
    weightCheckRequired = Column(String)
    weightSimulated = Column(Boolean,default = None)
    MinTemp = Column(String)
    Temp = Column(String)
    MaxTemp = Column(String)
    tempCheckRequired = Column(String)
    tempSimulated = Column(Boolean,default = None)
    foodImage =Column(String)
    foodImageSimulated = Column(Boolean,default = None)
    faceImage =Column(String)
    faceImageSimulated = Column(Boolean,default = None)
    live_temp = Column(String,default=None)
    live_weight = Column(String,default=None)
    TempSensor = Column(Boolean, nullable=False)
    weighingScale = Column(Boolean, nullable=False)
    foodCamera = Column(Boolean, nullable=False)
    faceCamera = Column(Boolean, nullable=False)
    clientServer = Column(Boolean, nullable=False)
    State = Column(String, nullable=False)
    QC_Result = Column(String)

    
class Logs(Base):
    __tablename__="dashboard" #changed from dash_new to dashboard
    S_No=Column(Integer,primary_key=True)
    order_id=Column(String(50))
    brand=Column(Integer,ForeignKey('brand.id'))
    zone=Column(Integer,ForeignKey('zone.id'))
    state=Column(Integer,ForeignKey('state.id'))
    city=Column(Integer,ForeignKey('city.id'))
    store=Column(Integer,ForeignKey('store.id'))
    Brand=relationship("Brand",back_populates="Logs")
    Zone=relationship("Zone",back_populates="Logs")
    State=relationship("State",back_populates="Logs")
    City=relationship("City",back_populates="Logs")
    Store=relationship("Store",back_populates="Logs")
    isVeg=Column(String(10))
    MinWeight=Column(String(10))
    Weight=Column(String(10))
    MaxWeight=Column(String(10))
    weightCheckRequired=Column(String(10))
    MinTemp=Column(String(10))
    Temp=Column(String(10))
    tempCheckRequired=Column(String(10))
    MaxTemp=Column(String(10))
    image=Column(String(100))
    date=Column(DateTime)
    date_no=Column(Integer)
    month_no=Column(Integer)
    week_day=Column(Integer)
    week_no=Column(Integer)
    year=Column(Integer)
    orderReceivedAt=Column(TIMESTAMP)
    timeTaken=Column(Integer)
    passed=Column(Integer)
    failed=Column(Integer)
    interval=Column(Integer)
