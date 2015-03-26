import conf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import common
import db
import time


        
Session=sessionmaker(bind=conf.param)
session_param=Session()
Session=sessionmaker(bind=conf.data)
session_data=Session()

com=common.cCommon()
com.task_launcher(session_param,session_data)

