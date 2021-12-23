import yaml

__config = None

def config():
    global __config
    if not __config:
        with open(file='./config.yaml',mode='r') as file:
            __config = yaml.safe_load(file)
    
    return __config