import db
import installer_conf


class install_imports(installer_conf.install):
    "installe les acquisition, ie les actions"
    def __init__(self,session):
        self.list_actions(session)
        
    def list_actions(self,session):
        '''
        installe les parametres d'acquisition
        :param session:
        '''
        print('\tImport :  CMDB')
        groupe=session.query(db.cGroupe).filter_by(name="Premier import").first()
        quoi=session.query(db.cQuoi).filter_by(module='import_file').filter_by(methode='xls').first()
        action=db.cAction(name='Import CMDB',\
            order=1,\
            base='CMDB',\
            ou='single',\
            groupe_fk=groupe.groupe_pk,\
            quoi_fk=quoi.quoi_pk)
        action.QuoiParams=[db.cQuoiParam(key='folder',value='h:\\python\\sample_data\\'),\
            db.cQuoiParam(key='file',value='CMDB.xls'),\
            db.cQuoiParam(key='sheet',value='7'),\
            db.cQuoiParam(key='cols_to_import',value='"CI Name","Reconciliation Identity","CI Type","Status","Address IP1","Address IP2","Address IP3","Address IP4","Master","Os","Processor","Floor","Room","Product Categorization Tier 1","Product Categorization Tier 2","Product Categorization Tier 3","Supported By"'),\
            db.cQuoiParam(key='output_format',value='dict'),\
            db.cQuoiParam(key='rename',value='0'),\
            db.cQuoiParam(key='format_date',value='1'),\
            ]
        action.Dicts=[\
            db.cDict(key='CI Name',value='ci_name'),\
            db.cDict(key='Reconciliation Identity',value='reconc_id'),\
            db.cDict(key='CI Type',value='ci_type'),\
            db.cDict(key='Status',value='ci_status'),\
            db.cDict(key='Address IP1',value='ip1'),\
            db.cDict(key='Address IP2',value='ip2'),\
            db.cDict(key='Address IP3',value='ip3'),\
            db.cDict(key='Address IP4',value='ip4'),\
            db.cDict(key='Master',value='master'),\
            db.cDict(key='Os',value='os'),\
            db.cDict(key='Processor',value='processor'),\
            db.cDict(key='Floor',value='floor'),\
            db.cDict(key='Room',value='room'),\
            db.cDict(key='Product Categorization Tier 1',value='categ1'),\
            db.cDict(key='Product Categorization Tier 2',value='categ2'),\
            db.cDict(key='Product Categorization Tier 3',value='categ3'),\
            db.cDict(key='Supported By',value='supported_by')\
            ] 
        session.add(action)
        print('\tImport : SLA')
        groupe=session.query(db.cGroupe).filter_by(name="Premier import").first()
        quoi=session.query(db.cQuoi).filter_by(module='import_file').filter_by(methode='xls').first()
        action=db.cAction(name='SLA',\
            order='2',\
            base='SLA',\
            ou='single',\
            groupe_fk=groupe.groupe_pk,\
            quoi_fk=quoi.quoi_pk)
        action.QuoiParams=[\
            db.cQuoiParam(key='folder',value='h:\\python\\sample_data\\'),\
            db.cQuoiParam(key='file',value='SLA.xlsx'),\
            db.cQuoiParam(key='sheet',value='2'),\
            db.cQuoiParam(key='cols_to_import',value='"CI Name","TIME SLOT","UNDERPINNING CONTRACT","Reconciliation Identity","BUSINESS CONTINUITY PLAN"'),\
            db.cQuoiParam(key='output_format',value='dict'),\
            db.cQuoiParam(key='rename',value='0'),\
            db.cQuoiParam(key='format_date',value='1'),\
            ]
        action.Dicts=[\
            db.cDict(key='CI Name',value='ci_name'),\
            db.cDict(key='TIME SLOT',value='time_slot'),\
            db.cDict(key='UNDERPINNING CONTRACT',value='contract'),\
            db.cDict(key='Reconciliation Identity',value='reconc_id'),\
            db.cDict(key='BUSINESS CONTINUITY PLAN',value='continuity_plan')\
            ]   
        session.add(action)
        print('\tImport :  CI_LIST')
        groupe=session.query(db.cGroupe).filter_by(name="Premier import").first()
        quoi=session.query(db.cQuoi).filter_by(module='import_file').filter_by(methode='xls').first()
        action=db.cAction(name='Import CI List',\
            order=8,\
            base='CI_LIST',\
            ou="single",\
            groupe_fk=groupe.groupe_pk,\
            quoi_fk=quoi.quoi_pk)
        action.QuoiParams=[db.cQuoiParam(key='folder',value='h:\\python\\sample_data\\'),\
            db.cQuoiParam(key='file',value='CI_LIST.xlsx'),\
            db.cQuoiParam(key='sheet',value='0'),\
            db.cQuoiParam(key='cols_to_import',value='"CI Name","Reconciliation Identity","CI Type","Status","Address IP1","Product Categorization Tier 3","Supported By","tld"'),\
            db.cQuoiParam(key='output_format',value='dict'),\
            db.cQuoiParam(key='rename',value='0'),\
            db.cQuoiParam(key='format_date',value='1'),\
            ]
        action.Dicts=[\
            db.cDict(key='CI Name',value='ci_name'),\
            db.cDict(key='Reconciliation Identity',value='reconc_id'),\
            db.cDict(key='CI Type',value='ci_type'),\
            db.cDict(key='Status',value='ci_status'),\
            db.cDict(key='Address IP1',value='ip1'),\
            db.cDict(key='tld',value='tld'),\
            db.cDict(key='Product Categorization Tier 3',value='categ3'),\
            db.cDict(key='Supported By',value='supported_by')\
            ] 
        session.add(action)
        
        print('\tImport :  Machines de rebond')
        groupe=session.query(db.cGroupe).filter_by(name="Premier import").first()
        quoi=session.query(db.cQuoi).filter_by(module='import_file').filter_by(methode='xls').first()
        action=db.cAction(name='Import Rebond',\
            order=10,\
            base='rebond',\
            ou='single',\
            groupe_fk=groupe.groupe_pk,\
            quoi_fk=quoi.quoi_pk)
        action.QuoiParams=[db.cQuoiParam(key='folder',value='h:\\python\\sample_data\\'),\
            db.cQuoiParam(key='file',value='rebond.xlsx'),\
            db.cQuoiParam(key='sheet',value='0'),\
            db.cQuoiParam(key='cols_to_import',value='"Name","Hostname","IP"'),\
            db.cQuoiParam(key='output_format',value='dict'),\
            db.cQuoiParam(key='rename',value='0'),\
            db.cQuoiParam(key='format_date',value='1'),\
            ]
        action.Dicts=[\
            db.cDict(key='Name',value='name'),\
            db.cDict(key='Hostname',value='hostname'),\
            db.cDict(key='IP',value='ip'),\
            ] 
        session.add(action)
        session.commit()    