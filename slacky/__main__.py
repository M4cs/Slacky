from slacky import config, client, Prefixes
from slacky.plugins import *
import slack
import httpx

print(Prefixes.event + 'Loading Plugins', end='\r')

class Commands:
    def __init__(self, **payload):
        self.commands = {
            'convinfo': convinfo(**payload),
            'winfo': winfo(**payload),
            'uinfo': uinfo(**payload),
            'errors': errors(**payload),
            'ani': animations(**payload),
            'stats': stats(**payload),
            'customrs': customrscmd(**payload),
            'ascii': ascii(**payload),
            'setstatus': status(**payload),
            'setprefix': setprefix(**payload),
            'help': shelp(**payload),
            'reactrand': reactrand(**payload),
            'reactspam': reactspam(**payload),
            'ud': ud(**payload),
            'space': space(**payload),
            'subspace': sub_space(**payload),
            'delete': delete(**payload),
            'shift': shift(**payload),
            'info': info(**payload),
            'howdoi': howdoicmd(**payload),
            'heartbeat': heartbeat(**payload),
            'react': react(**payload),
            'listener': listenercmd(**payload),
            'xkcd': xkcd(**payload)
        }
        
@slack.RTMClient.run_on(event='message')
def _commandListener(**payload):
    command = Commands(**payload)
    data = payload['data']
    user = data.get('user')
    text = data.get('text')
    if check_user(user):
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if command.commands.get(cmd.strip(config['prefix'])):
                return command.commands[cmd.strip(config['prefix'])]

@slack.RTMClient.run_on(event='message')
def _customrsd(**payload):
    return customrsd(**payload)

@slack.RTMClient.run_on(event='message')
def _listenerd(**payload):
    return listenerd(**payload)

def run_client(rtm):
    rtm.start()

slack_token = config['token']
rtmclient = slack.RTMClient(token=slack_token)
print(Prefixes.event + 'Default Plugins Loaded')
print(Prefixes.event + 'Custom Plugins Loaded (If Any)')
try:
    print(Prefixes.event + 'Running Bot...\n')
    run_client(rtmclient)
except KeyboardInterrupt:
    print(Prefixes.event + 'Shutdown Called')
    exit(0)
except Exception as e:
    bot.error(e)
    bot.error_count += 1
    run_client(rtmclient)