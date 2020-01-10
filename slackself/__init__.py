from slackself.config import load_config as lc
from slackself.api.auth import authenticate
from colorama import init
from colorama import Fore, Back, Style
import httpx, json

class Prefixes:
    info = str('[' + Fore.GREEN + 'INFO' + Style.RESET_ALL + ']')
    warning = str('[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + ']')
    event = str('[' + Fore.BLUE + 'EVENT' + Style.RESET_ALL + ']')
    error = str('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + ']')

config = lc()
if not config:
    print(Prefixes.error + 'No Config File Found. Make One Called config.json. Refer to Readme for template.')
    exit(1)
print(Prefixes.info + 'Config Loaded...')
print(Prefixes.info + 'Attempting to Authenticate with Slack...')
client = authenticate(config)
if not client:
    print(Prefixes.error + 'Could Not Authenticate with Slack! Please check your config and token!')
print(Prefixes.info + 'Authentication Successful...')