import sys
from sqlalchemy import create_engine,Column,BigInteger,Integer,String
from sqlalchemy.orm import sessionmaker, declarative_base
if sys.version_info >= (3, 7): from collections.abc import Iterable
else: from collections import Iterable

USERNAME=''
PASSWORD=''
HOST=''
PORT=3306
DATABASE=''
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)

engine=create_engine(
    DB_URI,
    echo=True,
    pool_pre_ping=True
)
Base=declarative_base()
class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    username=Column(String(255),nullable=False)
    password=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False)
    traffic=Column(BigInteger,nullable=False)
    proxies=Column(Integer,nullable=False)
    group=Column(String(255),nullable=False)
class Token(Base):
    __tablename__='tokens'
    id=Column(Integer,primary_key=True)
    username=Column(String(255),nullable=False)
    token=Column(String(255),nullable=False)
    status=Column(String(255),nullable=False)
class Node(Base):
    __tablename__='nodes'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(255), nullable=False)
    description=Column(String(255))
    hostname=Column(String(255), nullable=False)
    ip=Column(String(255), nullable=False)
    port=Column(Integer, nullable=False)
    admin_port=Column(Integer)
    admin_pass=Column(String(255))
    token=Column(String(255))
    group=Column(String(255))
    status=Column(String(255), nullable=False)
class Proxie(Base):
    __tablename__='proxies'
    id=Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String(255), nullable=False)
    proxy_name=Column(String(255), nullable=False)
    proxy_type=Column(String(5), nullable=False)
    local_ip=Column(String(255))
    local_port=Column(Integer)
    use_encryption=Column(String(5))
    use_compression=Column(String(5))
    domain=Column(String(255))
    locations=Column(String(255))
    host_header_rewrite=Column(String(255))
Base.metadata.create_all(bind=engine)

sem=sessionmaker(bind=engine)()

def model_to_dict(data):
    if data==None: return {}
    try:
        if isinstance(data, Iterable):
            tmp=[dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in data]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp=dict(zip(data.__dict__.keys(), data.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        sem.rollback()
        pass
    return []