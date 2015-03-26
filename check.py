from sqlalchemy.orm import sessionmaker

import conf
import db
import os


def ping(plugin_params,ou):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    out=dict()
    i=0
    ci_list=session_data.\
        query(eval('db.'+ou)).\
        filter(eval('db.'+ou+'.ci_type')=='Computer System').\
        filter(eval('db.'+ou+'.ci_status')=='Deployed').\
        filter(eval('db.'+ou+'.ip1')!='').\
        all()
    for ci in ci_list:
        tmp=dict()
        tmp['ci_name']=ci.ci_name
        tmp['hostname']=ci.ci_name
        tmp['ip']=ci.ip1
        ping=os.popen("ping -n 1 -w 2 "+ci.ip1)
        result=ping.readlines()
        if result[2].find('TTL')==-1:
            tmp['ping_status']=0
        elif (result[2].find('attente de la demande')==-1):
            tmp['ping_status']=0            
        else:
            tmp['ping_status']=1
        out[i]=tmp
        i=i+1
    return(out)
