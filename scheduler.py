import conf
import common
from sqlalchemy.orm import sessionmaker


        
Session=sessionmaker(bind=conf.param)
session_param=Session()

com=common.cCommon()
com.scheduler(session_param)


        

        