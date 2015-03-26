import conf
from sqlalchemy.orm import sessionmaker
import common


        
Session=sessionmaker(bind=conf.param)
session_param=Session()
Session_data=sessionmaker(bind=conf.data)
session_data=Session_data()

action_id=11



oCommon=common.cCommon()
oCommon.launch_action(action_id,session_param,session_data)

