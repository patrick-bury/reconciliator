import db
import installer_conf

class install_transfo(installer_conf.install):
    "Toutes les transformations"
    def __init__(self,session):
        ou='single'
        groupe=session.query(db.cGroupe).filter_by(name="Transfo").first()
        quoi=session.query(db.cQuoi).filter_by(module='transfo').filter_by(methode='launch').first()
        self.full_cmdb(session,ou,groupe,quoi)
        self.sla_erreurs(session,ou,groupe,quoi)
        self.doublons_cmdb(session,ou,groupe,quoi)
        self.ip_vides(session,ou,groupe,quoi)
        self.liste_serveur(session,ou,groupe,quoi)


    def full_cmdb(self,session,ou,groupe,quoi):
        print('\tTransfo : Full CMDB')

        # generate full CMDB
        action=db.cAction(name='full_cmdb',order='3',base='full_cmdb',ou=ou,groupe_fk=groupe.groupe_pk,quoi_fk=quoi.quoi_pk)
        action.TransfoDeps=[\
            db.cTransfoDep(base='CMDB'),\
            db.cTransfoDep(base='SLA')\
            ]
        action.QuoiParams=[\
            db.cQuoiParam(key='module',value='transfo_cmdb'),\
            db.cQuoiParam(key='methode',value='create_full'),\
            db.cQuoiParam(key='param1',value='test value'),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='reconc_id',value='reconc_id'),\
            db.cDict(key='ci_type',value='ci_type'),\
            db.cDict(key='ci_status',value='ci_status'),\
            db.cDict(key='time_slot',value='time_slot'),
            db.cDict(key='contract',value='contract'),\
            db.cDict(key='ip1',value='ip1'),\
            db.cDict(key='ip2',value='ip2'),\
            db.cDict(key='ip3',value='ip3'),\
            db.cDict(key='ip4',value='ip4'),\
            db.cDict(key='master',value='master'),\
            db.cDict(key='os',value='os'),\
            db.cDict(key='processor',value='processor'),\
            db.cDict(key='floor',value='floor'),\
            db.cDict(key='room',value='room'),\
            db.cDict(key='categ1',value='categ1'),\
            db.cDict(key='categ2',value='categ2'),\
            db.cDict(key='categ3',value='categ3'),\
            db.cDict(key='supported_by',value='supported_by'),\
            db.cDict(key='continuity_plan',value='continuity_plan')\
          ]
        session.add(action)
        session.commit()

    def sla_erreurs(self,session,ou,groupe,quoi):
        " search for bad values in a table"
        print('\tTransfo : erreurs pour les SLA')
        action=db.cAction(name='Erreurs pour les ASLA',order='4',base='bad_value_SLA',ou=ou,groupe_fk=groupe.groupe_pk,quoi_fk=quoi.quoi_pk)
        action.TransfoDeps=[\
            db.cTransfoDep(base='SLA')\
            ]
        action.QuoiParams=[\
            db.cQuoiParam(key='module',value='transfo_cmdb'),\
            db.cQuoiParam(key='methode',value='bad_value_SLA'),\
            db.cQuoiParam(key='bad',value="empty,unknown"),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='time_slot',value='time_slot'),
            db.cDict(key='contract',value='contract')\
            ]
        session.add(action)
        session.commit()

    def doublons_cmdb(self,session,ou,groupe,quoi):
        " recherche les doublons dans la CMDB "
        print('\tTransfo : Doublons dans la CMDB')
        action=db.cAction(name='Doublons CMDB',order='5',base='doublons_cmdb',ou=ou,groupe_fk=groupe.groupe_pk,quoi_fk=quoi.quoi_pk)
        action.TransfoDeps=[\
            db.cTransfoDep(base='CMDB')\
            ]
        action.QuoiParams=[\
            db.cQuoiParam(key='module',value='transfo_cmdb'),\
            db.cQuoiParam(key='methode',value='doublons_cmdb'),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='reconc_id',value='reconc_id')\
            ]
        session.add(action)
        session.commit()

    def ip_vides(self,session,ou,groupe,quoi):
        " cherche les ip vides "
        print('\tTransfo : IP vides')
        action=db.cAction(name='IP vides',order='6',base='empty_ip',ou=ou,groupe_fk=groupe.groupe_pk,quoi_fk=quoi.quoi_pk)
        action.TransfoDeps=[\
            db.cTransfoDep(base='CMDB')\
            ]
        action.QuoiParams=[\
            db.cQuoiParam(key='module',value='transfo_cmdb'),\
            db.cQuoiParam(key='methode',value='empty_ip'),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='ip1',value='ip1'),\
            db.cDict(key='ip2',value='ip2'),\
            db.cDict(key='ip3',value='ip3'),\
            db.cDict(key='ip4',value='ip4')\
            ]
        session.add(action)
        session.commit()

    def liste_serveur(self,session,ou,groupe,quoi):
        " extrait la liste des serveurs"
        print('\tTransfo : liste des serveurs')
        action=db.cAction(name='Liste des serveurs',active=0,order='7',base='server_list',ou=ou,groupe_fk=groupe.groupe_pk,quoi_fk=quoi.quoi_pk)
        action.TransfoDeps=[\
            db.cTransfoDep(base='CMDB')\
            ]
        action.QuoiParams=[\
            db.cQuoiParam(key='module',value='transfo_cmdb'),\
            db.cQuoiParam(key='methode',value='server_list'),\
            db.cQuoiParam(key='domain',value='patrick-bury.fr'),\
            ]
        action.Dicts=[\
            db.cDict(key='ci_name',value='ci_name'),\
            db.cDict(key='ip1',value='ip1'),
            db.cDict(key='ip_dns',value='ip_dns')\
            ]
        session.add(action)
        session.commit()

