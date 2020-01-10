from slackself import config, client, Prefixes
from slackself.plugins import *
import slack
import httpx

@slack.RTMClient.run_on(event='message')
def _heartbeat(**payload):
    return heartbeat(**payload)

@slack.RTMClient.run_on(event='message')
def _help(**payload):
    return help(**payload)

@slack.RTMClient.run_on(event='message')
def _reactrand(**payload):
    return reactrand(**payload)

@slack.RTMClient.run_on(event='message')
def _reactspam(**payload):
    return reactspam(**payload)

@slack.RTMClient.run_on(event='message')
def _howdoi(**payload):
    return howdoi(**payload)

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

slack_token = config['token']
rtmclient = slack.RTMClient(token=slack_token)
print(Prefixes.info + 'Bot Running')
print(Prefixes.info + 'Default Plugins Loaded: heartbeat, xkcd, react, info, shift, subspace, help')
rtmclient.start()