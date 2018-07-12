from sqlalchemy import Column, String, create_engine,BIGINT,INT,DATETIME,FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime
Base=declarative_base()

class Bus_runlog(Base):
    """训练日志信息"""
    #表名
    __tablename__='bus_runlog'
    #表的结构
    id=Column(String(255),primary_key=True)
    deleted=Column(INT)
    odr = Column(INT)
    acc = Column(FLOAT(5))
    CREATIONTIME = Column(DATETIME)
    info = Column(String(255))
    loss = Column(String(255))
    setp = Column(String(255))

#初始化数据库连接
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/framework')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)