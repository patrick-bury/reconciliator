import db

class install():
    "L'installeur, creee les tables, installe les differents parametres"
    def __init__(self,session):
        session.query(db.cAction).delete()
        session.query(db.cDbsource).delete()
        session.query(db.cDict).delete()
        session.query(db.cAction).delete()
        session.query(db.cWhen).delete()
        session.query(db.cGroupe).delete()
        session.query(db.cQuoi).delete()
        session.query(db.cQuoiParam).delete()
        session.commit()
        self.install_dbsource(session)
        self.install_quoi(session)
        self.install_groupe(session)
        

 
    def install_dbsource(self,session):
        print('\tPopulate dbsource')
        dbs=db.cDbsource(name='Essai',db_name='db_name',db_host='db_host',db_port='db_port',db_login='db_login',db_password='db_password')
        session.add(dbs)
        dbs=db.cDbsource(name='test',db_name='param',db_host='127.0.0.1',db_port=3306,db_login='root',db_password='')
        session.add(dbs)
        session.commit()
    def install_quoi(self,session):
        print('\tPopulate Quoi ')
        quoi=db.cQuoi(module='import_file',methode='xls')
        session.add(quoi)
        quoi=db.cQuoi(module='import_file',methode='csv')
        session.add(quoi)
        quoi=db.cQuoi(module='transfo',methode='launch')
        session.add(quoi)
        quoi=db.cQuoi(module='check',methode='ping')
        session.add(quoi)
        session.commit()
    def install_groupe(self,session):
        print('\tPopulate Declencheur & Groupe')
        grp=db.cGroupe(name='Transfo',decl_type='none',decl_value='')
        session.add(grp)
        grp=db.cGroupe(name='Premier import',decl_type='cron',decl_value='0 10 * * *')
        grp.cWhens=[db.cWhen(last_exec='0000-00-00 00:000:00',next_exec='0000-00-00 00:00:00')]
        session.add(grp)
        session.commit()
    def install_action(self,session):
        pass
        
    def install_transfo(self,session):
        pass

        

        
        
        


