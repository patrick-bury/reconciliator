class cDeclencheur:
    def __init__(self,nature):
        self.nature=nature
        print ('new declencheur')
    def show(self):
        print (self.nature)
    def set_date(self,heure):
        self.nature="temps"
        self.moment=heure
    def set_message(self,message):
        self.nature="message"    
        self.message="Go"
class cSource:
    def __init__(self,stype='bdd'):
        self.type= stype
        self.set_source()
    def set_source(self):
        if self.type=='bdd':
            self.source=cBdd()
        else:
            self.source=cBdd()
    def show(self):
        self.source.show()
            
class cBdd:
    def __init__(self,host='localhost',port='3306',user='root',passwd=''):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
    def show(self):
        print (self.host)
        print (self.port)
        print (self.user)
        print (self.passwd)
    def set_server(self,host='localhost',port='3306',user='root',passwd=''):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
class cSAppliqueA:
    def __init__(self,nom,ci,rebond):
        self.nom=nom
        self.ci_name=ci
        self.rebond=rebond
    def show(self):
        print(self.nom)
        print (self.ci_name)
        print (self.rebond)
class cSAppliqueOu:
    def __init__(self,nom,ip,auth_file="default_auth"):
        self.nom=nom
        self.ip=ip
        self.auth_file=auth_file
    def show(self):
        print (self.nom)
        print (self.ip)
        print (self.auth_file)
class cSAppliqueComment:
    def __init__(self,nom,plugin,action_id):
        self.nom=nom
        self.plugin=plugin
        self.action_id=action_id
    def show(self):
        print (self.nom)
        print (self.plugin)
class cRenvoieQuoi:
    def __init__(self,table):
        self.table=table
        self.dict=self.get_dict_for_table(table)
    def show(self):
        print (self.table)
        print (self.dict)
    def get_dict_for_table(self,table):
        a="oooo"
        return(a)
class cAction:
    def __init__(self,source,declencheur):
        self.get_action_id()
        self.source= cSource(source)
        self.declencheur = cDeclencheur(declencheur)
        self.sappliquea = cSAppliqueA("nom_ci","CI_XXXX","localhost")
        self.sappliqueou= cSAppliqueOu("rebond 1","10.0.0.1")
        self.sappliquecomment= cSAppliqueComment("plugin_1","get_unix",self.id)
        self.renvoiequoi= cRenvoieQuoi("table1")
    def show(self):
        print(self.id)
        self.source.show()
        self.declencheur.show()
        self.sappliquea.show()
        self.sappliqueou.show()
        self.sappliquecomment.show()
        self.renvoiequoi.show()
    def get_action_id(self):
        self.id=42
a = cAction('bdd','temps')
a.show()

        