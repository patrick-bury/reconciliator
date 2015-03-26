from crontab import CronTab
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import *
import mysql
from sqlalchemy  import *
import time
import installer_conf
import install_action
import install_transfo
import install_collect

import conf
import db

db.DropTables(conf.param)
conf.base_param.metadata.create_all(conf.param)        
Session=sessionmaker(bind=conf.param)
session=Session()
conf.base_data.metadata.create_all(conf.data)        
Session_data=sessionmaker(bind=conf.data)
session_data=Session_data()

print('Running Installer')
installation=installer_conf.install(session)
installation=install_action.install_imports(session)
installation=install_transfo.install_transfo(session)
installation=install_collect.install_collect(session)

print('Installation done')

conf.base_data.metadata.create_all(conf.data)        

