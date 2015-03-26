from sqlalchemy.orm import *
from sqlalchemy  import *
import conf
import sqlalchemy
import time

     


            
class cDbsource(conf.base_param):
    __tablename__='Dbsource'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        dbsource_pk=Column(Integer,primary_key=True,autoincrement=True)
        name=Column(String(255),unique=True)
        db_name=Column(String(255))
        db_host=Column(String(255))
        db_port=Column(String(255))
        db_login=Column(String(255))
        db_password=Column(String(255))
        __table_args__=(UniqueConstraint('db_name','db_host','db_port'),)
                          
            
class cQuoi(conf.base_param):
    __tablename__='Quoi'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        quoi_pk=Column(Integer,primary_key=True,autoincrement=True)
        module=Column(String(55))
        methode=Column(String(55))

class cMessage(conf.base_param):
    __tablename__='Message'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        message_pk=Column(Integer,primary_key=True,autoincrement=True)
        destinataire=Column(String(55))
        texte1=Column(String(255))
        texte2=Column(String(255))
        texte3=Column(String(255))
                
class cGroupe(conf.base_param): 
    __tablename__="Groupe"
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        groupe_pk=Column(Integer,primary_key=True,autoincrement=True)
        name=Column(String(255))
        decl_value=Column(String(255))
        decl_type=Column(String(255))
        decl_value=Column(String(255))
        
class cWhen(conf.base_param):
    __tablename__='When'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        when_pk=Column(Integer,primary_key=True,autoincrement=True)
        last_exec=Column(TIMESTAMP)
        next_exec=Column(TIMESTAMP)
        groupe_id=Column(Integer,ForeignKey('Groupe.groupe_pk'))
        groupe=relationship("cGroupe",backref=backref('cWhens',order_by=when_pk)) 
                   
class cAction(conf.base_param):
    __tablename__='Action'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        action_pk=Column(Integer,primary_key=True,autoincrement=True)
        name=Column(String(255))
        order=Column(Integer)
        base=Column(String(255))
        ou=Column(String(255))
        groupe_fk=Column(Integer,ForeignKey('Groupe.groupe_pk'))
        groupe=relationship('cGroupe')
        quoi_fk=Column(Integer,ForeignKey('Quoi.quoi_pk'))
        quoi=relationship('cQuoi')
        active=Column(Integer,default=1)

            
class cDict(conf.base_param):
    __tablename__="dict"
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        dict_pk=Column(Integer,primary_key=True,autoincrement=True)
        key=Column(String(255))
        value=Column(String(255))
        action_id=Column(Integer,ForeignKey(cAction.action_pk))
        action=relationship('cAction',backref=backref('Dicts',order_by=dict_pk))
        
    
            
class cQuoiParam(conf.base_param):
    __tablename__='Quoiparam'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        quoiparam_pk=Column(Integer,primary_key=True,autoincrement=True)
        key=Column(String(255))
        value=Column(Text)
        action_id=Column(Integer,ForeignKey(cAction.action_pk))
        action=relationship('cAction',backref=backref('QuoiParams',order_by=quoiparam_pk))

class cTaches(conf.base_param):
    __tablename__='Taches'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        taches_pk=Column(Integer,primary_key=True,autoincrement=True)
        name=Column(String(255))
        order=Column(Integer)
        action=Column(Integer)

                           
class cTransfoDep(conf.base_param):
    __tablename__='TransfoDep'
    try:
        __table__=Table(__tablename__,conf.base_param.metadata,autoload=True,autoload_with=conf.param)
    except:
        taches_pk=Column(Integer,primary_key=True,autoincrement=True)
        action_id=Column(Integer,ForeignKey(cAction.action_pk))
        action=relationship('cAction',backref=backref('TransfoDeps',order_by=taches_pk))
        base=Column(String(255))

                              
def DropTables(engine):
    cMessage.__table__.drop(conf.param,checkfirst=True)
    cQuoiParam.__table__.drop(conf.param,checkfirst=True)
    cTransfoDep.__table__.drop(conf.param,checkfirst=True)
    cWhen.__table__.drop(conf.param,checkfirst=True)
    cTaches.__table__.drop(conf.param,checkfirst=True)
    cDict.__table__.drop(conf.param,checkfirst=True)
    cAction.__table__.drop(conf.param,checkfirst=True)
    cQuoi.__table__.drop(conf.param,checkfirst=True)
    cGroupe.__table__.drop(conf.param,checkfirst=True)

#    CMDB.__table__.drop(conf.param,checkfirst=True)
#    SLA.__table__.drop(conf.param,checkfirst=True)
#    full_cmdb.__table__.drop(conf.param,checkfirst=True)


class CMDB(conf.base_data):
    __tablename__='CMDB'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        cmdb_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        reconc_id=Column(String(255))
        ci_type=Column(String(255))
        ci_status=Column(String(255))
        ip1=Column(String(255))
        ip2=Column(String(255))
        ip3=Column(String(255))
        ip4=Column(String(255))
        master=Column(String(255))
        os=Column(String(255))
        processor=Column(String(255))
        floor=Column(String(255))
        room=Column(String(255))
        categ1=Column(String(255))
        categ2=Column(String(255))
        categ3=Column(String(255))
        supported_by=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.reconc_id=to_store['reconc_id']
        self.ci_type=to_store['ci_type']
        self.ci_status=to_store['ci_status']
        self.ip1=to_store['ip1']
        self.ip2=to_store['ip2']
        self.ip3=to_store['ip3']
        self.ip4=to_store['ip4']
        self.master=to_store['master']
        self.os=to_store['os']
        self.processor=to_store['processor']
        self.floor=to_store['floor']
        self.room=to_store['room']
        self.categ1=to_store['categ1']
        self.categ2=to_store['categ2']
        self.categ3=to_store['categ3']
        self.supported_by=to_store['supported_by']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
        
class CI_LIST(conf.base_data):
    __tablename__='CI_LIST'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        ci_list_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        reconc_id=Column(String(255))
        ci_type=Column(String(255))
        ci_status=Column(String(255))
        ip1=Column(String(255))
        tld=Column(String(255))
        categ3=Column(String(255))
        supported_by=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.reconc_id=to_store['reconc_id']
        self.ci_type=to_store['ci_type']
        self.ci_status=to_store['ci_status']
        self.ip1=to_store['ip1']
        self.tld=to_store['tld']
        self.categ3=to_store['categ3']
        self.supported_by=to_store['supported_by']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")

         
class SLA(conf.base_data):
    __tablename__='SLA'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        sla_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        time_slot=Column(String(255))
        contract=Column(String(255))
        reconc_id=Column(String(255))
        continuity_plan=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.time_slot=to_store['time_slot']
        self.contract=to_store['contract']
        self.reconc_id=to_store['reconc_id']
        self.continuity_plan=to_store['continuity_plan']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
        
class full_cmdb(conf.base_data):
    __tablename__='full_cmdb'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        full_cmdb_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        reconc_id=Column(String(255))
        ci_type=Column(String(255))
        ci_status=Column(String(255))
        ip1=Column(String(255))
        ip2=Column(String(255))
        ip3=Column(String(255))
        ip4=Column(String(255))
        master=Column(String(255))
        os=Column(String(255))
        processor=Column(String(255))
        floor=Column(String(255))
        room=Column(String(255))
        categ1=Column(String(255))
        categ2=Column(String(255))
        categ3=Column(String(255))
        supported_by=Column(String(255))
        time_slot=Column(String(255))
        contract=Column(String(255))
        continuity_plan=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.reconc_id=to_store['reconc_id']
        self.ci_type=to_store['ci_type']
        self.ci_status=to_store['ci_status']
        self.ip1=to_store['ip1']
        self.ip2=to_store['ip2']
        self.ip3=to_store['ip3']
        self.ip4=to_store['ip4']
        self.master=to_store['master']
        self.os=to_store['os']
        self.processor=to_store['processor']
        self.floor=to_store['floor']
        self.room=to_store['room']
        self.categ1=to_store['categ1']
        self.categ2=to_store['categ2']
        self.categ3=to_store['categ3']
        self.supported_by=to_store['supported_by']
        self.time_slot=to_store['time_slot']
        self.contract=to_store['contract']
        self.continuity_plan=to_store['continuity_plan']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
                
class bad_value_SLA(conf.base_data):
    __tablename__='bad_value_SLA'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        bad_value_sla_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        time_slot=Column(String(255))
        contract=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.time_slot=to_store['time_slot']
        self.contract=to_store['contract']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
        
class doublons_cmdb(conf.base_data):
    __tablename__='doublons_cmdb'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        doublons_cmdb_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        reconc_id=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.reconc_id=to_store['reconc_id']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")


class empty_ip(conf.base_data):
    __tablename__='empty_ip'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        empty_ip_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        ip1=Column(String(255))
        ip2=Column(String(255))
        ip3=Column(String(255))
        ip4=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.ip1=to_store['ip1']
        self.ip2=to_store['ip2']
        self.ip3=to_store['ip3']
        self.ip4=to_store['ip4']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
        
        
class server_list(conf.base_data):
    __tablename__='server_list'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        server_list_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        ip1=Column(String(255))
        ip_dns=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.ip1=to_store['ip1']
        self.ip_dns=to_store['ip_dns']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
                
        
class rebond(conf.base_data):
    __tablename__='rebond'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        rebond_pk=Column(Integer,primary_key=True,autoincrement=True)
        name=Column(String(255))
        hostname=Column(String(255))
        ip=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.name=to_store['name']
        self.hostname=to_store['hostname']
        self.ip=to_store['ip']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")
        
class ping(conf.base_data):
    __tablename__='ping'
    try:
        __table__=Table(__tablename__,conf.base_data.metadata,autoload=True,autoload_with=conf.data)
    except:
        ping_pk=Column(Integer,primary_key=True,autoincrement=True)
        ci_name=Column(String(255))
        hostname=Column(String(255))
        ip=Column(String(255))
        ping_status=Column(String(255))
        import_order=Column(Integer,default=0)
        _acq_date=Column(TIMESTAMP)
    def __init__(self,to_store):
        self.ci_name=to_store['ci_name']
        self.hostname=to_store['hostname']
        self.ip=to_store['ip']
        self.ping_status=to_store['ping_status']
        self.import_order=-1
        self._acq_date=time.strftime("%Y-%m-%d %H:%M-%S")