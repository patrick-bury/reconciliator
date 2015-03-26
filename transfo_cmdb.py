import socket
import time

from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

import conf
from db import CMDB
import db


def create_full(plugin_params):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    results=session_data.query(db.CMDB,db.SLA).\
        outerjoin(db.SLA, db.CMDB.reconc_id==db.SLA.reconc_id).\
        filter(db.CMDB.import_order==-1).\
        group_by(db.CMDB.ci_name).all()
    i=0
    out=dict()
    for res in results:
        tmp=dict()
        tmp['ci_name']=res[0].ci_name
        tmp['ci_type']=res[0].ci_type
        tmp['ci_status']=res[0].ci_status
        tmp['ip1']=res[0].ip1
        tmp['ip2']=res[0].ip2
        tmp['ip3']=res[0].ip3
        tmp['ip4']=res[0].ip4
        tmp['master']=res[0].master
        tmp['os']=res[0].os
        tmp['processor']=res[0].processor
        tmp['floor']=res[0].floor
        tmp['room']=res[0].room
        tmp['categ1']=res[0].categ1
        tmp['categ2']=res[0].categ2
        tmp['categ3']=res[0].categ3
        tmp['reconc_id']=res[0].reconc_id
        tmp['supported_by']=res[0].supported_by
        if res[1] is None:
            tmp['time_slot']="N/A"
            tmp['contract']="N/A"
            tmp['continuity_plan']="N/A"
        else:
            tmp['time_slot']=res[1].time_slot
            tmp['contract']=res[1].contract
            tmp['continuity_plan']=res[1].continuity_plan
        out[i]=tmp
        i=i+1
    return(out)

def search_bad_values(session_data,table,column,bad_list):
    database=eval("db."+table+"."+column)
    import_order=eval("db."+table+".import_order")
    table=eval("db."+table)
    out=dict()
    i=0
    results=session_data.query(table).\
        filter(or_(database.is_(None),database=="",database.in_(bad_list))).\
        filter(import_order==-1).\
        all()
    for res in results:
        tmp=dict()
        tmp['ci_name']=res.ci_name
        tmp['time_slot']=res.time_slot
        tmp['contract']=res.contract
        out[i]=tmp
        i=i+1   
    
    return(out) 

def empty_ip(plugin_params):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    results=session_data.\
        query(db.CMDB).\
        filter(or_(db.CMDB.ip1=='',db.CMDB.ip2=='',db.CMDB.ip3=='',db.CMDB.ip4=='')).\
        filter(db.CMDB.import_order==-1).\
        filter(db.CMDB.ci_status=='Deployed').\
        filter(db.CMDB.ci_type=="Computer System").\
        all()
    i=0
    out=dict()
    for res in results:
        tmp=dict()
        tmp['ci_name']=res.ci_name
        tmp['ip1']=res.ip1
        tmp['ip2']=res.ip2
        tmp['ip3']=res.ip3
        tmp['ip4']=res.ip4
        out[i]=tmp 
        i=i+1
    return(out)
        
def bad_value_SLA(plugin_params):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    bad_list=plugin_params['bad'].split(',')
    out=dict()
    tmp=search_bad_values(session_data,'SLA','time_slot',bad_list)
    for elt in tmp:
        out[tmp[elt]['ci_name']]=tmp[elt] # on indexe sur le ci pour dedeboulonner
    tmp=search_bad_values(session_data,'SLA','contract',bad_list)
    for elt in tmp:
        out[tmp[elt]['ci_name']]=tmp[elt]  # on indexe sur le ci pour dedeboulonner
    # on renomme les index
    final=dict()
    i=0
    for elt in out:
        final[i]=out[elt]
        i=i+1
    return(final)

def doublons_cmdb(plugin_params):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    i=0
    out=dict() 
    res=session_data.query(db.CMDB).\
        filter(db.CMDB.import_order==-1).\
        group_by(db.CMDB.ci_name).\
        having(func.count(CMDB.ci_name) > 1).\
        all()
    for key in res:
        results=session_data.query(db.CMDB).\
            filter(db.CMDB.ci_name==key.ci_name).\
            filter(db.CMDB.import_order==-1).\
            all()
        for tt in results:
            tmp=dict()
            tmp['ci_name']=tt.ci_name
            tmp['reconc_id']=tt.reconc_id
            out[i]=tmp
            i=i+1
    res=session_data.query(db.CMDB).\
        filter(db.CMDB.import_order==-1).\
        group_by(db.CMDB.reconc_id).\
        having(func.count(CMDB.reconc_id) > 1).\
        all()
    for key in res:
        results=session_data.query(db.CMDB).\
            filter(db.CMDB.ci_name==key.ci_name).\
            filter(db.CMDB.import_order==-1).\
            all()
        for tt in results:
            tmp=dict()
            tmp['ci_name']=tt.ci_name
            tmp['reconc_id']=tt.reconc_id
            out[i]=tmp
            i=i+1    
    return(out)
        
def server_list(plugin_params):
    conf.base_param.metadata.create_all(conf.param)
    Session=sessionmaker(bind=conf.data)
    session_data=Session()
    domain=plugin_params['domain']
    i=0
    out=dict() 
    results=session_data.\
        query(db.CMDB).\
        filter(db.CMDB.import_order==-1).\
        filter(db.CMDB.ci_status=='Deployed').\
        filter(db.CMDB.ci_type=="Computer System").\
        all()
    for tt in results:
        tmp=dict()
        tmp['ci_name']=tt.ci_name
        tmp['ip1']=tt.ip1
        try:
            tmp['ip_dns']=socket.gethostbyname(tt.ci_name+domain)
        except:
            tmp['ip_dns']=''
        out[i]=tmp
        i=i+1    
    return(out)


