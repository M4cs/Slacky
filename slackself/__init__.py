from slackself.config import load_config as lc
from slackself.api.auth import authenticate
from colorama import init
from colorama import Fore, Back, Style
import httpx, json, logging

class Prefixes:
    info = str('[' + Fore.GREEN + 'INFO' + Style.RESET_ALL + ']')
    warning = str('[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + ']')
    event = str('[' + Fore.BLUE + 'EVENT' + Style.RESET_ALL + ']')
    error = str('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + ']')

class Listeners:
    def __init__(self, config):
        self.listeners = config['listeners']

    def add(self, phrase):
        self.listeners.append(phrase)
        with open('config.json', 'r+') as file:
            obj = json.load(file)
            obj['listeners'] = self.listeners
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()
    
    def delete(self, phrase):
        num = self.listeners.index(phrase)
        del self.listeners[num]
        with open('config.json', 'r+') as file:
            obj = json.load(file)
            obj['listeners'] = self.listeners
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()


config = lc()
if not config:
    print(Prefixes.error + 'No Config File Found. Make One Called config.json. Refer to Readme for template.')
    exit(1)
print(Prefixes.info + 'Config Loaded...')
print(Prefixes.info + 'Attempting to Authenticate with Slack...')
listener = Listeners(config)
client = authenticate(config)
if not client:
    print(Prefixes.error + 'Could Not Authenticate with Slack! Please check your config and token!')
print(Prefixes.info + 'Authentication Successful...')
logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger('slacky')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('listener.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
