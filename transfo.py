import transfo_cmdb

def launch(plugin_params):
    results=getattr(eval(plugin_params['module']),plugin_params['methode'])(plugin_params)
    print('Transfo %s Completed' % plugin_params['methode'])
    return(results)    
    