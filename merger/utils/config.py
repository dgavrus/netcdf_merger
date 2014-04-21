

class ConfigAttributes:
    pass

def parse_config():
    attributes = ConfigAttributes()
    config_file = open("config", 'r');
    config = config_file.readlines()
    for i in xrange(len(config)):
        if config[i].startswith('path'):
            attributes.path = config[i].split()[1]
    config_file.close()
    return attributes
            