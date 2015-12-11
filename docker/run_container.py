import os 
import pexpect

def run_container(config_docker):
    cmd1='docker rm -f {0}'.format(config_docker['name'])
    print cmd1
    os.popen(cmd1).read()
    port_mapping=' '.join(['-p {0}:{1}'.format(x[0],x[1]) for x in config_docker['port_mapping']])
    volume_mapping=' '.join(['-v {0}:{1}'.format(x[0],x[1]) for x in config_docker['volume_mapping']])
    environment=' '.join(['-e {0}={1}'.format(x[0],x[1]) for x in config_docker['environment']])
    links=' '.join(['--link {0}:{1}'.format(x[0],x[1]) for x in config_docker['links']])
    expose=' '.join(['--expose {0}'.format(x) for x in config_docker['expose']])
    options=''
    if config_docker.get('options'):
        options=config_docker.get('options')
    if config_docker['config_templates']:
        config_templates=' '.join(['-v {0}:/templates/f{1}'.format(x[1],x[0]) for x in enumerate(config_docker['config_templates'])])
        cmd_config='docker run --rm=True {0} {1} {2} tonibagur/config_environ'.format(environment,links,config_templates)
        print cmd_config
        os.popen(cmd_config)
    cmd_start=config_docker.get('cmd','')
    cmd2='docker run {0} --rm=True {1} --name {2} {3} {4} {5} {6} {7} {8}'.format(port_mapping,volume_mapping,config_docker['name'],links,environment,expose,options,config_docker['image'],cmd_start)
    print cmd2
    process=pexpect.spawn(cmd2)
    process.interact()

