from run_container import run_container
import os


dirname=os.path.dirname
code_volume=dirname(os.popen('pwd').read())
print "code_volume",code_volume

config_docker={
    'port_mapping':[['8888','8888']],
    'config_templates':[],
    'links':[],
    'volume_mapping':[
        [code_volume,'/code'],
    ],
    'environment':[],
    'expose':[],
    'name':'astql',
    'image':'tonibagur/jupyter',
    'options':'-ti',
    'cmd':'/bin/bash'
}


if __name__=='__main__':
    run_container(config_docker)
