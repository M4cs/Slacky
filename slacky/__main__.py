from slacky import config, client, Prefixes, bot
from slacky.api.auth import CookieWebClient
from slacky.plugins import *
from time import sleep
import re
import logging

# Use slack_bolt for Socket Mode (listening)
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Suppress verbose logging
logging.basicConfig(level=logging.WARNING)

print(Prefixes.event + 'Loading Plugins')

# Commands dictionary
commands = {
    'heartbeat': lambda **payload: heartbeat,
    'ping': lambda **payload: ping,
    'stats': lambda **payload: stats,
    'setprefix': lambda **payload: setprefix,
    'space': lambda **payload: space,
    'winfo': lambda **payload: winfo,
    'uinfo': lambda **payload: uinfo,
    'convinfo': lambda **payload: convinfo,
    'ani': lambda **payload: animations,
    'errors': lambda **payload: errors,
    'ud': lambda **payload: ud,
    'help': lambda **payload: shelp,
    'delete': lambda **payload: delete,
    'ascii': lambda **payload: ascii,
    'reactrand': lambda **payload: reactrand,
    'reactspam': lambda **payload: reactspam,
    'customrs': lambda **payload: customrscmd,
    'howdoi': lambda **payload: howdoicmd,
    'subspace': lambda **payload: sub_space,
    'xkcd': lambda **payload: xkcd,
    'react': lambda **payload: react,
    'info': lambda **payload: info,
    'shift': lambda **payload: shift,
    'status': lambda **payload: status,
    'listener': lambda **payload: listenercmd,
    'msgstatus': lambda **payload: msgstatus,
    'stockpic': lambda **payload: stockpic,
    'coronastatus': lambda **payload: coronavirus
}

# Create the Bolt app with bot token for receiving events
app = App(token=config['bot_token'])

# Create user client for sending messages as yourself
user_token = config['token']
cookies = f'd={config["d_cookie"]}'
if 'd_s_cookie' in config:
    cookies += f'; d-s={config["d_s_cookie"]}'
user_client = CookieWebClient(token=user_token, cookies=cookies)

# Override the global client with user_client so plugins use it
import slacky
slacky.client = user_client


def process_command(event, say):
    """Process incoming messages and execute commands"""
    prefix = config['prefix']
    text = event.get('text', '')
    user_id = event.get('user', '')

    # Only respond to messages from the configured user
    if user_id != config['user']:
        return

    # Check for command
    cmd_match = re.search(r'{}(.*?) |{}(.*?)$'.format(re.escape(prefix), re.escape(prefix)), text)
    if not cmd_match:
        return

    cmd = cmd_match.group(1) if cmd_match.group(1) else cmd_match.group(2)

    if cmd in commands:
        # Build payload similar to RTM format
        payload = {
            'data': event,
            'web_client': user_client,
            'rtm_client': None
        }
        func = commands.get(cmd)()
        if func:
            try:
                func(**payload)
            except Exception as e:
                bot.error(e)


def process_custom_replies(event):
    """Process custom replies"""
    payload = {
        'data': event,
        'web_client': user_client,
        'rtm_client': None
    }
    try:
        customrsd(**payload)
    except Exception as e:
        bot.error(e)


def process_listeners(event):
    """Process listeners"""
    payload = {
        'data': event,
        'web_client': user_client,
        'rtm_client': None
    }
    try:
        listenerd(**payload)
    except Exception as e:
        bot.error(e)


@app.event("message")
def handle_message_events(event, say):
    """Handle all message events"""
    # Skip bot messages and message_changed events
    if event.get('subtype') in ['bot_message', 'message_changed', 'message_deleted']:
        return

    process_command(event, say)
    process_custom_replies(event)
    process_listeners(event)


print(Prefixes.event + 'Default Plugins Loaded')
print(Prefixes.event + 'Custom Plugins Loaded (If Any)')

if __name__ == "__main__":
    try:
        print(Prefixes.event + 'Running Bot (Socket Mode)...')
        print(Prefixes.start + 'Log Output:')

        # Start Socket Mode handler
        handler = SocketModeHandler(app, config['app_token'])
        handler.start()

    except KeyboardInterrupt:
        print(Prefixes.event + 'Shutdown Called')
        exit(0)
    except Exception as e:
        bot.error(e)
        print(Prefixes.error + str(e))
        exit(1)
