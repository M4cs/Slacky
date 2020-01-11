from slacky import config, client, Prefixes
from slacky.plugins import *
import slack
import httpx

print(Prefixes.event + 'Loading Plugins', end='\r')

@slack.RTMClient.run_on(event='message')
def _heartbeat(**payload):
    return heartbeat(**payload)

@slack.RTMClient.run_on(event='message')
def _help(**payload):
    return shelp(**payload)

@slack.RTMClient.run_on(event='message')
def _ascii(**payload):
    return ascii(**payload)

@slack.RTMClient.run_on(event='message')
def _reactrand(**payload):
    return reactrand(**payload)

@slack.RTMClient.run_on(event='message')
def _reactspam(**payload):
    return reactspam(**payload)

@slack.RTMClient.run_on(event='message')
def _howdoi(**payload):
    return howdoicmd(**payload)

@slack.RTMClient.run_on(event='message')
def _subspace(**payload):
    return sub_space(**payload)

@slack.RTMClient.run_on(event='message')
def _xkcd(**payload):
    return xkcd(**payload)

@slack.RTMClient.run_on(event='message')
def _react(**payload):
    return react(**payload)

@slack.RTMClient.run_on(event='message')
def _info(**payload):
    return info(**payload)

@slack.RTMClient.run_on(event='message')
def _shift(**payload):
    return shift(**payload)

@slack.RTMClient.run_on(event='message')
def _listenercmd(**payload):
    return listenercmd(**payload)

@slack.RTMClient.run_on(event='message')
def _listenerd(**payload):
    return listenerd(**payload)

@slack.RTMClient.run_on(event='message')
def _status(**payload):
    return status(**payload)

slack_token = config['token']
rtmclient = slack.RTMClient(token=slack_token)
print(Prefixes.event + 'Default Plugins Loaded')
print(Prefixes.event + 'Custom Plugins Loaded (If Any)')
try:
    print(Prefixes.event + 'Running Bot...\n')
    rtmclient.start()
except KeyboardInterrupt:
    print(Prefixes.event + 'Shutdown Called')
    exit(0)