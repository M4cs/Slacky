from slacky import config, config_path
import re, json

class CustomBinds:
    def __init__(self, config):
        try:
            self.binds = config['binds']
        except KeyError:
            self.binds = []

    def add(self, bind):
        with open(config_path, 'r+') as file:
            obj = json.load(file)
            match = False
            for bind_info in self.binds:
                if bind_info['bind_key'] == bind['bind_key']:
                    bind_info['paste'] = bind['paste']
                    match = True
            if not match:
                self.binds.append(bind)
            obj['binds'] = self.binds
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()
    
    def delete(self, num):
        del self.binds[int(num)]
        with open(config_path, 'r+') as file:
            obj = json.load(file)
            obj['binds'] = self.binds
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()

custombinds = CustomBinds(config)
