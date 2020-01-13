from slacky import config, client, Prefixes, listener, check_user, customrs, bot
from slacky.constants.emojis import emojis
from slacky.plugins.custom import *
from slack.errors import SlackApiError
from terminaltables import DoubleTable
from howdoi import howdoi
from pyfiglet import Figlet
import json
import slack
import httpx
import time
import random
import re

def stats(**payload):
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
            if cmd == config['prefix'] + 'stats':
                print(Prefixes.event + 'Ran command: stats')
                bot.command_count += 1
                workspace = client.team_info()['team']['name']
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":slack: *Slacky Bot Statistics:*"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": ":clock1: Uptime: *{}*".format(bot.get_uptime())
                            },
                            {
                                "type": "mrkdwn",
                                "text": ":bangbang: *Error Count*: *{}*".format(bot.error_count)
                            },
                            {
                                "type": "mrkdwn",
                                "text": ":keyboard: *Command Count*: *{}*".format(bot.command_count)
                            },
                            {
                                "type": "mrkdwn",
                                "text": ":warning: *Warning Count*: *{}*".format(bot.warning_count)
                            },
                            {
                                "type": "mrkdwn",
                                "text": ":computer: *Current Workspace*: *{}*".format(workspace)
                            },
                            {
                                "type": "mrkdwn",
                                "text": ":eyes: *Msgs Parsed*: *{}*".format(bot.message_count)
                            }
                        ]
                    }
                ]
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        blocks=blocks
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))

def customrscmd(**payload):
    bot.message_count += 1
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
            if cmd == config['prefix'] + 'customrs':
                print(Prefixes.event + 'Ran Command: customrs')
                bot.command_count += 1
                if len(text_split) < 2:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="Missing Arguments. Check the wiki for more information.",
                            ts=timestamp
                        )
                        bot.warning_count += 1
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                else:
                    action = text_split[1]
                    if action == "add":
                        if len(text_split) < 4:
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Missing Arguments. Check the wiki for more information.",
                                    ts=timestamp
                                )
                                bot.warning_count += 1
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                        else:
                            ans = re.findall(r'["“‘\'](.*?)[\'’”"]',  text)
                            trigger = ans[0]
                            reply = ans[1]
                            is_strict = text_split[-1]
                            if is_strict == "strict":
                                is_strict = True
                            else:
                                is_strict = False
                            custom_r = {
                                'trigger': trigger,
                                'reply': reply,
                                'is_strict': is_strict
                            }
                            customrs.add(custom_r)
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Added Custom Reply. Trigger is \"{}\" and Reply will be \"{}\".\nStrict: {}".format(trigger, reply, is_strict),
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                    elif action == "delete":
                        if len(text_split) < 3:
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Missing Arguments. Check the wiki for more information.",
                                    ts=timestamp
                                )
                                bot.warning_count += 1
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                        else:
                            num = text_split[2]
                            customrs.delete(num)
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Deleted Custom Reply.",
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                    elif action == "list":
                        blocks = []
                        if len(customrs.custom_replies) > 0:
                            for custom_reply in customrs.custom_replies:
                                blocks.append({
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*#*: {}\n*Trigger:* {}\n*Reply:* {}\n*Strict:* {}".format(customrs.custom_replies.index(custom_reply), custom_reply['trigger'], custom_reply['reply'], custom_reply['is_strict'])
                                    }
                                })
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    blocks=blocks,
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                        else:
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="No Custom Replies Set! Add some to your config or use the customrs command.",
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1

def customrsd(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    text = data.get('text')
    if text:
        if user != config['user']:
            if not config['prefix'] in text:
                for custom_reply in customrs.custom_replies:
                    if not custom_reply['is_strict']:
                        if text.lower() in custom_reply['trigger'].lower():
                            try:
                                client.chat_postMessage(
                                    channel=channel_id,
                                    text=custom_reply['reply'],
                                    as_user=True,
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
                    else:
                        if text.lower() == custom_reply['trigger'].lower():
                            try:
                                client.chat_postMessage(
                                    channel=channel_id,
                                    text=custom_reply['reply'],
                                    as_user=True,
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                print(Prefixes.error + str(e))
                                bot.error_count += 1
    
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
            if cmd == config['prefix'] + 'ascii':
                print(Prefixes.event + 'Ran Command: ascii')
                bot.command_count += 1
                if len(text_split) < 2:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="You need to feed a string to asciify!",
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                else:
                    rest = ' '.join(text_split[1:])
                    f = Figlet(font='slant')
                    ascii_text = f.renderText(rest)
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="```{}```".format(ascii_text),
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
    
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
            if cmd == config['prefix'] + 'setstatus':
                if len(text_split) < 3:
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    print(Prefixes.event + 'Ran Command: setstatus')
                    bot.command_count += 1
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
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="Failed to set status.",
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            print(Prefixes.error + str(e))
                            bot.error_count += 1

def setprefix(**payload):
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
            if cmd == config['prefix'] + 'setprefix':
                print(Prefixes.event + 'Ran Command: setprefix')
                bot.command_count += 1
                if len(text_split) != 2:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="Please only feed one argument for your prefix. You can repeat special chars to act as a longer prefix.",
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                else:
                    prefix = text_split[1]
                    config['prefix'] = prefix
                    with open('config.json', 'r+') as file:
                        obj = json.load(file)
                        obj['prefix'] = prefix
                        file.seek(0)
                        json.dump(obj, file, indent=4)
                        file.truncate()
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="Updated Prefix to: `{}`".format(prefix),
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1

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
            if cmd == config['prefix'] + 'help':
                print(Prefixes.event + 'Ran Command: help')
                bot.command_count += 1
                table = [
                    ['Command', 'Description', 'Usage'],
                    ['help', 'Display this message', '~help'],
                    ['heartbeat', 'Check if bot is up or not', '~heartbeat'],
                    ['info', 'Get info about the bot', '~info'],
                    ['stats', 'Get stats about the bot running', '~stats'],
                    ['customrs', 'Set custom replies for messages.', 'Read Wiki'],
                    ['ascii', 'Generate ASCII Art from Text', '~ascii <phrase>'],
                    ['space', 'Add spaces between characters', '~space <phrase>'],
                    ['shift', 'CrEaTe ShIfT tExT lIkE tHiS', '~shift <phrase>'],
                    ['subspace', 'Replace spaces with emojis', '~subspace <:emoji:> <msg>'],
                    ['setstauts', 'Set status of your profile', '~setstatus <:emoji:> <status>'],
                    ['setprefix', 'Set prefix for commands (Default ~)', '~setprefix <prefix>'],
                    ['xkcd', 'Get Daily xkcd comic', '~xkcd'],
                    ['react', 'React to last sent message', '~react :emoji:'],
                    ['reactrand', 'React to with random emoji', '~reactrand'],
                    ['reactspam', 'Spam 23 Reactions (Notification Spam)', '~randspam'],
                    ['delete', 'Delete # of msgs', '~delete msg_count'],
                    ['howdoi', 'Find code snippets from stack overflow', '~howdoi loop over list python'],
                    ['listener', 'Add or remove listeners', '~listener <add/delete> <phrase>'],
                    ['listener list', 'List all listener words', '~listener list'],
                ]
                ttable = DoubleTable(table)
                str_table = str(ttable.table)
                new_tb = str_table.split('\n')
                str_table = ""
                for line in new_tb:
                    if not "═" in line:
                        str_table += str(line + '\n')
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(str(str_table)),
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1

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
            if cmd == config['prefix'] + 'reactrand':
                print(Prefixes.event + 'Ran Command: reactrand')
                bot.command_count += 1
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1
                conv_info = client.conversations_history(channel=channel_id, count=1)
                latest_ts = conv_info['messages'][0]['ts']
                try:
                    web_client.reactions_add(
                        channel=channel_id,
                        timestamp=latest_ts,
                        name=random.choice(emojis)
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1

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
            if cmd == config['prefix'] + 'reactspam':
                print(Prefixes.event + 'Ran Command: reactspam')
                bot.command_count += 1
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1
                conv_info = client.conversations_history(channel=channel_id, count=1)
                latest_ts = conv_info['messages'][0]['ts']
                for _ in range(23):
                    try:
                        web_client.reactions_add(
                            channel=channel_id,
                            timestamp=latest_ts,
                            name=random.choice(emojis)
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                        
def ud(**payload):
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
            if cmd == config['prefix'] + 'ud':
                print(Prefixes.event + 'Ran Command: ud')
                bot.command_count += 1
                if len(text_split) < 2:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    api = 'http://urbanscraper.herokuapp.com/define/'
                    term = '+'.join(text_split[1:])
                    query = str(api + term)
                    res = httpx.get(query).json()
                    definition = res['definition']
                    url = res['url']
                    blocks = [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "*Urban Dictionary Definition For:* {}\n\n{}\n\n<{}|Link To Entry>".format(term, definition, url)
                            }
                        }
                    ]
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            ts=timestamp,
                            blocks=blocks
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                        
def space(**payload):
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
            if cmd == config['prefix'] + 'space':
                if len(text_split) < 2:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    rest = ' '.join(text_split[1:])
                    new_string = ""
                    for char in rest:
                        new_string += str(char + " ")
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            ts=timestamp,
                            text=new_string
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))

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
            if cmd == config['prefix'] + 'subspace':
                print(Prefixes.event + 'Ran Command: subspace')
                bot.command_count += 1
                if len(text_split) < 3:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    emoji = text_split[1]
                    rest = ' '.join(text_split[2:])
                    rest = rest.replace(' ', ' {} '.format(emoji))
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text=rest,
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1
                        
def delete(**payload):
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
            if cmd == config['prefix'] + 'delete':
                web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                )
                if len(text_split) < 2:
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    print(Prefixes.event + 'Ran Command: delete')
                    bot.command_count += 1
                    msgs = int(text_split[1])
                    conv_hist = web_client.conversations_history(channel=channel_id, count=msgs if msgs <= 100 else 100)
                    msg_ts = []
                    for i in conv_hist['messages']:
                        for k, v in i.items():
                            if k == "user" and v == config['user']:
                                msg_ts.append(i['ts'])
                    for ts in msg_ts:
                        try:
                            web_client.chat_delete(
                                channel=channel_id,
                                ts=ts
                            )
                        except SlackApiError as e:
                            print(Prefixes.error + str(e))
                            bot.error_count += 1
                        

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
            if cmd == config['prefix'] + 'shift':
                print(Prefixes.event + 'Ran Command: shift')
                bot.command_count += 1
                if len(text_split) < 2:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    print(Prefixes.error + 'Missing Arguments! Please read the help menu for more info!')
                    bot.warning_count += 1
                else:
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
                    except SlackApiError as e:
                        print(Prefixes.error + str(e))
                        bot.error_count += 1

def info(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        if str(config['prefix'] + 'info') == data.get('text', []):
            print(Prefixes.event + 'Ran Command: info')
            bot.command_count += 1
            try:
                web_client.chat_update(
                    channel=channel_id,
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": """\
Running :slack: *Slacky* by <https://twitter.com/maxbridgland|Max Bridgland>

To See Commands Run: {}help

*Source Code*: <https://github.com/M4cs/Slacky|GitHub>
*Wiki*: <https://github.com/M4cs/Slacky/wiki|GitHub Wiki>""".format(config['prefix'])
                        }
                    }],
                    ts=timestamp
                )
            except SlackApiError as e:
                print(Prefixes.error + str(e))
                bot.error_count += 1

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
            if cmd == config['prefix'] + 'howdoi':
                print(Prefixes.event + 'Ran Command: howdoi')
                bot.command_count += 1
                if len(text_split) < 2:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    print(Prefixes.error + 'Missing Arguments! Please read the help menu for more info!')
                    bot.warning_count += 1
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="Finding the answer to that...",
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1
                parser = howdoi.get_parser()
                args = vars(parser.parse_args(text_split[1:]))
                output = howdoi.howdoi(args)
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(output),
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1

def heartbeat(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        if str(config['prefix'] + 'heartbeat') == data.get('text', []):
            print(Prefixes.event + 'Ran Command: heartbeat')
            bot.command_count += 1
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="I'm Alive!",
                    ts=timestamp
                )
            except SlackApiError as e:
                print(Prefixes.error + str(e))
                bot.error_count += 1

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
            if cmd == config['prefix'] + 'react':
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1
                emoji = text_split[1]
                print(Prefixes.event + 'Ran Command: react')
                bot.command_count += 1
                conv_info = client.conversations_info(channel=channel_id)
                latest = conv_info['channel']['latest']
                latest_ts = latest['ts']
                try:
                    web_client.reactions_add(
                        channel=channel_id,
                        timestamp=latest_ts,
                        name=emoji
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1

def listenerd(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    text = data.get('text')
    if text:
        if not config['prefix'] in text:
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
            if cmd == config['prefix'] + 'listener':
                if len(text_split) == 1:
                    print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
                    bot.warning_count += 1
                else:
                    action = text_split[1]
                    phrase = ' '.join(text_split[2:])
                    if action == 'add':
                        listener.add(phrase)
                        print(Prefixes.event + 'Listener Added:', phrase)
                        bot.command_count += 1
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="`{}` added to listeners.".format(phrase),
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            print(Prefixes.error + str(e))
                            bot.error_count += 1
                    elif action == 'list':
                        bot.command_count += 1
                        listeners = ""
                        for ear in listener.listeners:
                            listeners += str(ear + '\n')
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="```{}```".format(listeners),
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            print(Prefixes.error + str(e))
                            bot.error_count += 1
                    elif action == 'delete':
                        listener.delete(phrase)
                        bot.command_count += 1
                        print(Prefixes.event + 'Listener Deleted:', phrase)
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="`{}` removed from listeners.".format(phrase),
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            print(Prefixes.error + str(e))
                            bot.error_count += 1

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
            if cmd == config['prefix'] + 'xkcd':
                bot.command_count += 1
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
                                    "text": alt_text,
                                    "emoji": True
                                },
                                "image_url": link,
                                "alt_text": alt_text
                            }
                        ],
                        ts=timestamp
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))
                    bot.error_count += 1