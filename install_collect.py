import db
import installer_conf


class install_collect(installer_conf.install):
    def __init__(self,session):
        self.list_actions(session)
        
    def list_actions(self,session):
        print('\tCollect :  IP')
        groupe=session.query(db.cGroupe).filter_by(name="Premier import").first()
        quoi=session.query(db.cQuoi).filter_by(module='check').filter_by(methode='ping').first()
        action=db.cAction(name='Test Ping',\
            order=11,\
            base='ping',\
            ou='CI_LIST',\
            groupe_fk=groupe.groupe_pk,\
            quoi_fk=quoi.quoi_pk)
        action.QuoiParams=[db.cQuoiParam(key='msg',value='hello world'),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='hostname',value='hostname'),\
            db.cDict(key='ip',value='ip'),\
            db.cDict(key='ping_status',value='ping_status'),\
            ] 
        session.add(action)
        session.commit()