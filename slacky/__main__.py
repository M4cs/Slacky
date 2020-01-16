from slacky import config, client, Prefixes
from slacky.plugins import *
from time import sleep
import slack
import httpx
import re

print(Prefixes.event + 'Loading Plugins')

commands = {
        'heartbeat': lambda **payload: heartbeat,
        'ping': lambda **payload: ping,
        'stats' : lambda **payload: stats,
        'setprefix': lambda **payload: setprefix,
        'space' : lambda **payload: space,
        'winfo': lambda **payload: winfo,
        'uinfo' : lambda **payload: uinfo,
        'convinfo': lambda **payload: convinfo,
        'ani' : lambda **payload: animations,
        'errors': lambda **payload: errors,
        'ud' : lambda **payload: ud,
        'help': lambda **payload: shelp,
        'delete' : lambda **payload: delete,
        'ascii': lambda **payload: ascii,
        'reactrand' : lambda **payload: reactrand,
        'reactspam': lambda **payload: reactspam,
        'customrs' : lambda **payload: customrscmd,
        'howdoi': lambda **payload: howdoicmd,
        'subspace' : lambda **payload: sub_space,
        'xkcd': lambda **payload: xkcd,
        'react' : lambda **payload: react,
        'info': lambda **payload: info,
        'shift' : lambda **payload: shift,
        'status': lambda **payload: status,
        'listener': lambda **payload: listenercmd,
        'msgstatus': lambda  **payload: msgstatus
    }

@slack.RTMClient.run_on(event='message')
def _cmdcheck(**payload):
    prefix = config['prefix']
    text = payload['data'].get('text')
    if not text:
        return "no text"
    cmd = re.search(r'{}(.*?) |{}(.*?)$'.format(prefix, prefix), text)
    if not cmd:
        return "no command"
    cmd = cmd.group(1) if cmd.group(1) else cmd.group(2)
    if cmd in commands.keys():
        func = commands.get(cmd)()
        if func:
            return func(**payload)

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
    print(Prefixes.event + 'Running Bot...')
    print(Prefixes.start + 'Log Output:')
    rtmclient.ping_interval = 2
    run_client(rtmclient)
except KeyboardInterrupt:
    print(Prefixes.event + 'Shutdown Called')
    exit(0)
# except Exception as e:
#     bot.error(e)
#     bot.error_count += 1
#     print(Prefixes.event + 'Attempting To Auto Reconnect...')
#     time.sleep(2)
#     run_client(rtmclient)
