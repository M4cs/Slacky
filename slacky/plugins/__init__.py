from slacky import config, client, Prefixes, listener
from slacky.constants.emojis import emojis
from slack.errors import SlackApiError
from terminaltables import AsciiTable
from howdoi import howdoi
from pyfiglet import Figlet
import json
import slack
import httpx
import time
import random

def check_user(user):
    if user == config['user']:
        return True
    else:
        return False
    
def ascii(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~ascii':
                rest = ' '.join(text_split[1:])
                f = Figlet(font='slant')
                ascii_text = f.renderText(rest)
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(ascii_text),
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')
    
def status(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~setstatus':
                if len(text_split) == 3:
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                else:
                    print(Prefixes.event + 'Ran Command: setstatus')
                    emoji = text_split[1]
                    phrase = ' '.join(text_split[2:])
                    try:
                        web_client.users_profile_set(
                            profile= {
                                "status_text": phrase,
                                "status_emoji": emoji,
                                "status_expiration": 0
                        })
                        web_client.chat_update(
                                channel=channel_id,
                                text="Set Status Successfully!",
                                ts=timestamp
                        )
                    except SlackApiError:
                        print(Prefixes.error + 'Unable To Set Status!')
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="Failed to set status.",
                                ts=timestamp
                            )
                        except SlackApiError:
                            print(Prefixes.error + 'Failed To Update Message!')
                    
def shelp(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~help':
                print(Prefixes.event + 'Ran Command: help')
                table = [
                    ['Command', 'Description', 'Usage'],
                    ['heartbeat', 'Check if bot is up or not', '~heartbeat'],
                    ['info', 'Get info about the bot', '~info'],
                    ['shift', 'CrEaTe ShIfT tExT lIkE tHiS', '~shift <phrase>'],
                    ['subspace', 'Replace spaces with emojis', '~subspace <:emoji:> <msg>'],
                    ['setstauts', 'Set status of your profile', '~setstatus <:emoji:> <status>'],
                    ['xkcd', 'Get Daily xkcd comic', '~xkcd'],
                    ['react', 'React to last sent message', '~react :emoji:'],
                    ['reactrand', 'React to with random emoji', '~reactrand'],
                    ['reactspam', 'Spam 23 Reactions (Notification Spam)', '~randspam'],
                    ['howdoi', 'Find code snippets from stack overflow', '~howdoi loop over list python'],
                    ['listener', 'Add or remove listeners', '~listener <add/delete> <phrase>'],
                    ['listener list', 'List all listener words', '~listener list'],
                    ['help', 'Display this message', '~help']
                ]
                ttable = AsciiTable(table)
                str_table = str(ttable.table)
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(str_table),
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def reactrand(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~reactrand':
                print(Prefixes.event + 'Ran Command: reactrand')
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Delete Your Message!')
                conv_info = client.conversations_info(channel=channel_id)
                latest = conv_info['channel']['latest']
                latest_ts = latest['ts']
                try:
                    web_client.reactions_add(
                        channel=channel_id,
                        timestamp=latest_ts,
                        name=random.choice(emojis)
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To React To Message!')

def reactspam(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~reactspam':
                print(Prefixes.event + 'Ran Command: reactspam')
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Delete Your Message!')
                conv_info = client.conversations_info(channel=channel_id)
                latest = conv_info['channel']['latest']
                latest_ts = latest['ts']
                for i in range(23):
                    try:
                        web_client.reactions_add(
                            channel=channel_id,
                            timestamp=latest_ts,
                            name=random.choice(emojis)
                        )
                    except SlackApiError:
                        print(Prefixes.error + 'Failed To React To Message!')

def sub_space(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~subspace':
                print(Prefixes.event + 'Ran Command: subspace')
                emoji = text_split[1]
                rest = ' '.join(text_split[2:])
                rest = rest.replace(' ', ' {} '.format(emoji))
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text=rest,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def shift(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~shift':
                print(Prefixes.event + 'Ran Command: shift')
                rest = ' '.join(text_split[1:])
                new_text = ""
                count = 0
                for char in rest:
                    if count == 0:
                        new_text += char.upper()
                        count = 1
                    else:
                        new_text += char.lower()
                        count = 0
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text=new_text,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def info(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        if '~info' == data.get('text', []):
            print(Prefixes.event + 'Ran Command: info')
            try:
                web_client.chat_update(
                    channel=channel_id,
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": """\
Running :slack: *Slacky* by <https://twitter.com/maxbridgland|Max Bridgland>

To See Commands Run: *~help*

*Source Code*: <https://github.com/M4cs/Slacky|GitHub>"""
                        }
                    }],
                    ts=timestamp
                )
            except SlackApiError:
                print(Prefixes.error + 'Failed To Send Message!')

def howdoicmd(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~howdoi':
                print(Prefixes.event + 'Ran Command: howdoi')
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="Finding the answer to that...",
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')
                parser = howdoi.get_parser()
                args = vars(parser.parse_args(text_split[1:]))
                output = howdoi.howdoi(args)
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(output),
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def heartbeat(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        if '~heartbeat' == data.get('text', []):
            print(Prefixes.event + 'Ran Command: heartbeat')
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="I'm Alive!",
                    ts=timestamp
                )
            except SlackApiError:
                print(Prefixes.error + 'Failed To Send Message!')

def react(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~react':
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Delete Your Message!')
                emoji = text_split[1]
                print(Prefixes.event + 'Ran Command: react')
                conv_info = client.conversations_info(channel=channel_id)
                latest = conv_info['channel']['latest']
                latest_ts = latest['ts']
                try:
                    web_client.reactions_add(
                        channel=channel_id,
                        timestamp=latest_ts,
                        name=emoji
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To React To Message!')

def listenerd(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    text = data.get('text')
    if text:
        if not "~" in text:
            if len(listener.listeners) >= 1:
                if any(x in text for x in listener.listeners):
                    print(Prefixes.event + 'Listener Triggered! Message:', text, '| Channel ID:', channel_id)

def listenercmd(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~listener':
                if len(text_split) == 1:
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                else:
                    action = text_split[1]
                    phrase = ' '.join(text_split[2:])
                    if action == 'add':
                        listener.add(phrase)
                        print(Prefixes.event + 'Listener Added:', phrase)
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="`{}` added to listeners.".format(phrase),
                                ts=timestamp
                            )
                        except SlackApiError:
                            print(Prefixes.error + 'Failed To Send Message!')
                    elif action == 'list':
                        listeners = ""
                        for ear in listener.listeners:
                            listeners += str(ear + '\n')
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="```{}```".format(listeners),
                                ts=timestamp
                            )
                        except SlackApiError:
                            print(Prefixes.error + 'Failed To Send Message!')
                    elif action == 'delete':
                        listener.delete(phrase)
                        print(Prefixes.event + 'Listener Deleted:', phrase)
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="`{}` removed from listeners.".format(phrase),
                                ts=timestamp
                            )
                        except SlackApiError:
                            print(Prefixes.error + 'Failed To Send Message!')

def xkcd(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~xkcd':
                print(Prefixes.event + 'Ran Command: xkcd')
                res = httpx.get('https://xkcd.com/info.0.json').json()
                link = res['img']
                alt_text = res['alt']
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        blocks=[
                            {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": "Today's xkcd Comic",
                                    "emoji": True
                                },
                                "image_url": link,
                                "alt_text": alt_text
                            }
                        ],
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')