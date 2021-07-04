from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/KMS', pool_recycle=14400)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import sessionmaker, relationship, exc

Session = sessionmaker()
Session.configure(bind=engine)
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Sequence, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.mysql import LONGBLOB, TINYINT
import datetime


class Zone(Base):
    __tablename__ = 'zone'
    id = Column("id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    State = relationship("State")
    Orders = relationship("Orders")


class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    zone = Column(Integer, ForeignKey('zone.id', ondelete='CASCADE'), nullable=False)
    Zone = relationship("Zone", back_populates="State")
    City = relationship("City")
    Orders = relationship("Orders")


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(Integer, ForeignKey('state.id', ondelete='CASCADE'), nullable=False)
    State = relationship("State", back_populates="City")
    Store = relationship("Store")
    Orders = relationship("Orders")


class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    client_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    city = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'), nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    City = relationship("City", back_populates="Store")
    Machine = relationship("Machine")
    Orders = relationship("Orders")


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    brandImage = Column(String(150))
    Orders = relationship("Orders")
    Product = relationship("Product")


class Product(Base):
    __tablename__ = 'product_utility'
    id = Column(Integer, primary_key=True)
    brandId = Column(Integer, ForeignKey('brand.id'))
    minTemp = Column(Integer)
    maxTemp = Column(Integer)
    productName = Column(String(100))
    tempCheckReq = Column(Boolean)
    weightCheckReq = Column(Boolean)
    isVeg = Column(Boolean)
    refImage = Column(String(150))
    minWeight = Column(Integer)
    maxWeight = Column(Integer)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
    Brand = relationship("Brand", back_populates="Product")


# Orders = relationship("Orders")


class Machine(Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True)
    store = Column(Integer, ForeignKey('store.id', ondelete='CASCADE'), nullable=False)
    mac = Column(String(17), nullable=False)
    serial_number = Column(String, nullable=False)
    model_number = Column(String, nullable=False)
    manufactured_on = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    installed_on = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    warranty_expires_on = Column(DateTime, default=datetime.datetime.utcnow())
    software_version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())
    Store = relationship("Store", back_populates="Machine")
    Orders = relationship("Orders")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    email = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    Orders = relationship("Orders")


class Live(Base):
    __tablename__ = 'live'
    mac = Column(String, nullable=False, primary_key=True)
    machine = Column(Integer, nullable=False)
    user = Column(Integer, nullable=False)
    updatedAt = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow())
    lastQcAt = Column(TIMESTAMP)
    orderId = Column(String)
    productName = Column(String)
    isVeg = Column(String)
    MinWeight = Column(String)
    Weight = Column(String)
    MaxWeight = Column(String)
    weightCheckRequired = Column(String)
    MinTemp = Column(String)
    Temp = Column(String)
    MaxTemp = Column(String)
    tempCheckRequired = Column(String)
    faceImage = Column(String)
    #faceLabel = Column(String)
    #foodBoxImage = Column(String)
    foodImage = Column(String)
    #foodLabel = Column(String)
    live_temp = Column(String, default=None)
    live_weight = Column(String, default=None)
    TempSensor = Column(TINYINT, nullable=False)
    weighingScale = Column(TINYINT, nullable=False)
    faceCamera = Column(TINYINT, nullable=False)
    foodCamera = Column(TINYINT, nullable=False)
    clientServer = Column(TINYINT, nullable=False)
    State = Column(String, nullable=False)
    QC_Result = Column(String)


class Orders(Base):
    __tablename__ = 'dashboard'
    S_No = Column(Integer, primary_key=True)
    order_id = Column(String, nullable=False)
    user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    productId = Column(Integer)
    productName = Column(String, nullable=False)
    brand = Column(Integer, ForeignKey('brand.id', ondelete='CASCADE'), nullable=False)
    zone = Column(Integer, ForeignKey('zone.id', ondelete='CASCADE'), nullable=False)
    state = Column(Integer, ForeignKey('state.id', ondelete='CASCADE'), nullable=False)
    city = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'), nullable=False)
    store = Column(Integer, ForeignKey('store.id', ondelete='CASCADE'), nullable=False)
    machine = Column(Integer, ForeignKey('machine.id', ondelete='CASCADE'), nullable=False)
    isVeg = Column(TINYINT, nullable=False)
    MinWeight = Column(Integer, nullable=False)
    Weight = Column(Integer, nullable=False)
    MaxWeight = Column(Integer, nullable=False)
    weightCheckRequired = Column(TINYINT, nullable=False)
    MinTemp = Column(Integer, nullable=False)
    Temp = Column(Integer, nullable=False)
    MaxTemp = Column(Integer, nullable=False)
    tempCheckRequired = Column(TINYINT, nullable=False)
    foodImage = Column(String, nullable=False)
    #foodBoxLabel = Column(String, nullable=False)
    faceImage = Column(String, nullable=False)
    #faceLabel = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    date_no = Column(Integer, nullable=False)
    month_no = Column(Integer, nullable=False)
    week_day = Column(Integer, nullable=False)
    week_no = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    orderReceivedAt = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow())
    timeTaken = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow())
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    interval = Column(Integer, nullable=False, default=0)
    Zone = relationship("Zone", back_populates="Orders")
    State = relationship("State", back_populates="Orders")
    City = relationship("City", back_populates="Orders")
    Store = relationship("Store", back_populates="Orders")
    Machine = relationship("Machine", back_populates="Orders")
    Brand = relationship("Brand", back_populates="Orders")
    # Product = relationship("Product",back_populates="Orders")
