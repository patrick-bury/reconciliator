from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy  import create_engine

param=create_engine('mysql+mysqlconnector://root@localhost/param?charset=utf8&use_unicode=0')
base_param = declarative_base(param)

data=create_engine('mysql+mysqlconnector://root@localhost/data?charset=utf8&use_unicode=0')
base_data = declarative_base(data)
