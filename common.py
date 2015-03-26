import db
from sqlalchemy import func
import import_file
import transfo
import check
import time
from croniter import croniter 
from datetime import datetime

class cCommon():
    def get_params(self,session,action_id):
        quoiparam=session.query(db.cQuoiParam).filter_by(action_id=action_id).all()
        plugin_param=dict()  
        for param in quoiparam:
            plugin_param.update({param.key:param.value})
        return(plugin_param)
        
    def get_dictionnary(self,session,action_id):
        _dict=session.query(db.cDict).filter_by(action_id=action_id).all()
        dico=dict()
        for entry in _dict:
            dico.update({entry.value:entry.key})
        return(dico)
    
    def search_action_info(self,session,action_id):
        result=dict()
        res=session.query(db.cAction,db.cQuoi).\
                join(db.cQuoi,db.cQuoi.quoi_pk==db.cAction.quoi_fk).\
                filter(db.cAction.action_pk==action_id).\
                first()
        result['module']=res[1].module
        result['methode']=res[1].methode
        result['db']=res[0].base
        result['ou']=res[0].ou
        return(result)
    
    def StoreResults(self,results,dico,tablename,session):
        self.Historize(tablename,session)
        for result in results:
            db_name="db."+tablename
            to_store=dict()
            for value in dico:
                if isinstance(results[result][dico[value]], str):
                    to_store[value]=results[result][dico[value]]
                elif isinstance(results[result][dico[value]], int):
                    to_store[value]=results[result][dico[value]]
                else:
                    to_store[value]=results[result][dico[value]].decode('utf8')
            dummy=eval(db_name)(to_store)
            try:
                session.add(dummy)
            except:
                session.rollback()
            session.commit()

    def Historize(self,tablename,session):
        base=eval("db."+tablename)
        maxi=session.query(func.max(base.import_order)).scalar()
        if isinstance(maxi,int):
            if (maxi==-1):
                maxi=1
            else:
                maxi=maxi+1
        else:
            maxi=1
        session.query(base).filter(base.import_order==-1).update({"import_order":maxi})
    
    def launch_action(self,action_id,session_param,session_data):
        # get params
        action=self.search_action_info(session_param,action_id)
        dico=self.get_dictionnary(session_param,action_id)
        plugin_param=self.get_params(session_param,action_id)
        # launch action
        if (action['ou']=='single'):
            results=getattr(eval(action['module']),action['methode'])(plugin_param)
        else:
            results=getattr(eval(action['module']),action['methode'])(plugin_param,action['ou'])
            
        # store results
        if (results!="dummy"):
            self.StoreResults(results,dico,action['db'],session_data)
            
    def scheduler_empty_next(self,session,now):
        res=session.query(db.cWhen).all()
        for groupes in res:
            if groupes.next_exec==None:
                when=db.cWhen()
                session.query(db.cWhen).filter_by(when_pk=groupes.when_pk).delete()
                when=db.cWhen(last_exec='0000-00-00 00:00:00',next_exec=now,groupe_id=groupes.groupe_id)
                session.add(when)
                session.commit()
        # schedule les groupes nouveaux
        res=session.query(db.cGroupe).filter(db.cGroupe.name!='Transfo').all()
        for groupes in res:
            res2=session.query(db.cWhen).filter_by(groupe_id=groupes.groupe_pk).count()
            if res2==0:
                when=db.cWhen(last_exec='0000-00-00 00:00:00',next_exec=now,groupe_id=groupes.groupe_pk)
                session.add(when)
                session.commit()
                
    def scheduler_prepare_next(self,session,a_scheduler,now,w):
        for job in a_scheduler:
            cron=croniter(a_scheduler[job],datetime.now())
            next_exec=cron.get_next(datetime)
            dummy=session.query(db.cWhen).filter_by(when_pk=w.when_pk).update({"last_exec":now})
            dummy=session.query(db.cWhen).filter_by(when_pk=w.when_pk).update({"next_exec":next_exec})
            session.commit()
                    
    def scheduler_what_to_do(self,session,now):
        # cherche la liste des actions a mener
        a_scheduler=dict()
        oOrder=session.query(func.max(db.cTaches.order).label("max_order")).first()
        if (isinstance(oOrder,int)):
            max_order=oOrder.max_order
        else:
            max_order=0
        job=0    
        for g,w,a in session.query(db.cGroupe,db.cWhen,db.cAction).\
                join(db.cWhen,db.cWhen.groupe_id==db.cGroupe.groupe_pk).\
                join(db.cAction,db.cAction.groupe_fk==db.cGroupe.groupe_pk).\
                filter(db.cGroupe.name!='Transfo').\
                filter(db.cAction.active==1).\
                all():
            if time.time()>time.mktime(w.next_exec.timetuple()) + w.next_exec.microsecond / 1E6:
                print("We have job to schedule %s " % a.name)
                order=max_order+a.order
                tache=db.cTaches(name=a.name,order=order,action=a.action_pk)
                session.add(tache)
                session.commit()
                a_scheduler.update({g.groupe_pk:g.decl_value})
                job=1
        if job==0:
            print("Nothing to Schedule")
        # on re schedule le boulot pour la prochaine fois
        self.scheduler_prepare_next(session,a_scheduler,now,w)
                
    def scheduler(self,session):
        # verifie si un next_exec existe, sinon, on le creee
        now=time.strftime("%Y-%m-%d %H:%M-%S")
        self.scheduler_empty_next(session,now)
        self.scheduler_what_to_do(session,now)

  

    def task_launcher(self,session_param,session_data):
        while(1):
            nb_task=session_param.query(func.count(db.cTaches.action).label('nb_taches')).first()
            if (nb_task.nb_taches!=0):
                task=session_param.query(db.cTaches).order_by(db.cTaches.order).first()
                print("Task %s launched" % task.name)
                #launch task
                self.launch_action(task.action,session_param,session_data)
                # remove from taches
                session_param.query(db.cTaches).filter(db.cTaches.taches_pk==task.taches_pk).delete()
                session_param.commit()
                #search for depedancies
                oBase=session_param.query(db.cAction).filter(db.cAction.action_pk==task.action).first()
                for action in session_param.query(db.cTransfoDep).\
                        filter(db.cTransfoDep.base==oBase.base).\
                        all():
                    oName=session_param.query(db.cAction).filter(db.cAction.action_pk==action.action_id).first()
                    oOrder=session_param.query(func.max(db.cTaches.order).label("max_order")).first()
                    if (oName.active==1):
                        new_task=db.cTaches(name=oName.name,action=action.action_id,order=oOrder.max_order)
                        session_param.add(new_task)
                        session_param.commit()
            else:
                print("No more tasks to execute, sleep 5 seconds")
                time.sleep(5)    
 

