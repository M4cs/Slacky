from slacky import config, client, Prefixes, listener, check_user, customrs, bot, version
from slacky.constants.emojis import emojis
from slack.errors import SlackApiError
from terminaltables import DoubleTable
from howdoi import howdoi
from threading import Thread
from pyfiglet import Figlet
from io import BytesIO
import requests
import pandas as pd
import json
import slack
import httpx
import time
import random
import re
import glob
import os
import ntpath

def cmd_setup(command, **payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data.get('ts')
    web_client = client
    text = data.get('text')
    if text and check_user(user):
        text_split = text.split(' ')
        cmd = text_split[0]
        if cmd == config['prefix'] + command:
            print(Prefixes.event + 'Ran Command: {}'.format(command))
            bot.command_count += 1
            return data, channel_id, user, timestamp, web_client, text, text_split
        else:
            return None, None, None, None, None, None, None
    else:
        return None, None, None, None, None, None, None
    
from slacky.plugins.custom import *

def coronavirus(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('coronastatus', **payload)
    if data:
        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text="One Second"
            )
        except SlackApiError as e:
            bot.error(e)
        csv_content = requests.get('https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/export?usp=sharing&format=csv').content
        df = pd.read_csv(BytesIO(csv_content), index_col=0)
        places = df['Country/Region']
        confirmed = df['Confirmed']
        deaths = df['Deaths']
        recovered = df['Recovered']
        total_confirm = confirmed.sum()
        total_deaths = deaths.sum()
        total_recov = recovered.sum()
        region_dict = {}
        for place, confirm, death in zip(places, confirmed, deaths):
            if region_dict.get(place):
                region_dict[place]['confirms'] = int(region_dict[place].get('confirms')) + int(confirm) if str(confirm).lower() != 'nan' else 0
                region_dict[place]['deaths'] = int(region_dict[place].get('deaths')) + int(death) if str(death).lower() != 'nan' else 0
            else:
                region_dict[place] = {
                    'confirms': int(confirm) if str(confirm).lower() != 'nan' else 0,
                    'deaths': int(death) if str(death).lower() != 'nan' else 0,
                }
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '*Status of Coronavirus:*'
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': ':mask: *Confirmed Cases: {}*'.format(int(total_confirm))
                    },
                    {
                        'type': 'mrkdwn',
                        'text': ':skull: *Deaths: {}*'.format(int(total_deaths))
                    },
                    {
                        'type': 'mrkdwn',
                        'text': ':muscle: *Recovered: {}*'.format(int(total_recov))
                    }
                ]
            }
        ]
        blocks.append({"type": "section", "fields": []})
        count = 0
        for k, v in region_dict.items():
            if count == 10:
                break
            blocks[2]['fields'].append({
                "type": "mrkdwn",
                "text": "*Region:* {}\n*Confirmed:* {}\n*Deaths:* {}\n==================\n".format(k, region_dict[k]['confirms'], region_dict[k]['deaths'])
            })
            count += 1
        blocks.append({"type": "section", "fields": []})
        new_count = 0
        for k, v in region_dict.items():
            if new_count >= count:
                blocks[3]['fields'].append({
                    "type": "mrkdwn",
                    "text": "*Region:* {}\n*Confirmed:* {}\n*Deaths:* {}\n=================\n".format(k, region_dict[k]['confirms'], region_dict[k]['deaths'])
                })
            new_count += 1

        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                attachments=[{
                    'color': '#f43d2d',
                    'blocks': blocks
                }]
            )
        except SlackApiError as e:
            bot.error(e)
    
def ping(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('ping', **payload)
    if data:
        real_ts = float(timestamp)
        now = float(time.time())
        relay = int(float(now - real_ts) * 1000)
        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text='',
                attachments=[
                    {
                        "color": "#f8f33a",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": ":signal_strength: *Response Time:* {}ms".format(relay)
                                }
                            }
                        ]
                    }
                ]
            )
        except SlackApiError as e:
            bot.error(e)

def msgstatus(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('msgstatus', **payload)
    if data:
        if bot.msgstatus:
            bot.msgstatus = False
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="On-Message Status Change Disabled"
                )
            except SlackApiError as e:
                bot.error(e)
        else:
            bot.msgstatus = True
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="On-Message Status Change Enabled"
                )
            except SlackApiError as e:
                bot.error(e)
                
def winfo(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('winfo', **payload)
    if data:
        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text="Getting Workspace Info.."
            )
        except SlackApiError as e:
            bot.error(e)
        try:
            t_info = web_client.team_info()
        except SlackApiError as e:
            bot.error(e)
        try:
            chan_count = 0
            cursor = ""
            while True:
                c_info = web_client.conversations_list(limit=100,cursor=cursor)
                for _ in c_info['channels']:
                    chan_count += 1
                if c_info.get('response_metadata').get("next_cursor"):
                    cursor = c_info['response_metadata'].get("next_cursor")
                    pass
                else:
                    break
        except SlackApiError as e:
            bot.error(e)
        
        if t_info and chan_count:
            team = t_info['team']
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":slack: *Team Info for {}:*".format(team['name'])
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": team['icon']['image_230'],
                        "alt_text": "Team Icon"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*ID:* {}".format(team['id'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Domain:* {}.slack.com".format(team['domain'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*E-Mail Format:* email@{}".format(team.get('email_domain') if team.get('email_domain') else "N/A")
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Enterprise Name:* {}".format(team.get('enterprise_name') if team.get('enterprise_name') else 'N/A')
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Channel Count:* {}".format(chan_count)
                        }
                    ]
                }
            ]
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    attachments=[
                        {
                            'color': '#0f87ff',
                            'blocks': blocks
                        }
                    ]
                )
            except SlackApiError as e:
                bot.error(e)
            
            

def uinfo(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('uinfo', **payload)
    if data:
        if len(text_split) != 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="Correct syntax is: `uinfo @user`"
                )
            except SlackApiError as e:
                bot.error(e)
        else:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="Getting User Info.."
                )
            except SlackApiError as e:
                bot.error(e)
            try:
                user_list = client.users_list()
            except SlackApiError as e:
                bot.error(e)
            if user_list:
                query = text_split[1].split('@')[1].split('>')[0]
                match = None
                for wuser in user_list['members']:
                    if wuser['id'] == query:
                        match = wuser
                        break
                if match:
                    blocks = [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': ':slack: *User Information:*'
                            }
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': '*Name:* {}\n*Status:* {}'.format(match['real_name'], match['profile'].get('status_text') if match['profile'].get('status_text') else 'N/A')
                            },
                            'fields': [
                                {
                                    'type': 'mrkdwn',
                                    'text': '*Title:* {}'.format(match['profile'].get('title') if match['profile'].get('title') else 'N/A')
                                },
                                {
                                    'type': 'mrkdwn',
                                    'text': '*Username:* {}'.format(match['name'])
                                },
                                {
                                    'type': 'mrkdwn',
                                    'text': '*E-Mail:* {}'.format(match['profile']['email'])
                                },
                                {
                                    'type': 'mrkdwn',
                                    'text': '*Timezone:* {}'.format(match['tz_label'])
                                },
                                {
                                    'type': 'mrkdwn',
                                    'text': '*Phone:* {}'.format(match['profile'].get('phone') if match['profile'].get('phone') else 'N/A')
                                }
                            ],
                            'accessory': {
                                'type': 'image',
                                'image_url': match['profile'].get('image_512'),
                                'alt_text': 'Profile Picture'
                            }
                        }
                    ]
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            ts=timestamp,
                            attachments=[{
                                'color': '#0f87ff',
                                'blocks': blocks
                            }]
                        )
                    except SlackApiError as e:
                        bot.error(e)
                
                else:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            ts=timestamp,
                            text="No User Found."
                        )
                    except SlackApiError as e:
                        bot.error(e)

def errors(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('errors', **payload)
    if data:
        if len(bot.errors) > 0:
            blocks = [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': '*Slacky Bot Errors:*'
                    }
                }       
            ]
            msg = ""
            for error in bot.errors:
                msg += str(error + '\n')
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '```' + msg + '```'
                }
            })
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    attachments=[{
                        'color': '#0f87ff',
                        'blocks': blocks
                    }]
                )
            except SlackApiError as e:
                bot.error(e)
                
        else:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text='No Errors Triggered!'
                )
            except SlackApiError as e:
                bot.error(e)
                            

def animations(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('ani', **payload)
    if data:
        if len(text_split) < 2:
            try:
                web_client.chat_delete(
                    channel=channel_id,
                    ts=timestamp
                )
            except SlackApiError as e:
                bot.error(e)
                
        else:
            if len(text_split) == 2:
                loop = 1
            elif len(text_split) == 3:
                loop = int(text_split[2])
            target_file = None
            for file in glob.glob('animations/*.txt'):
                if ntpath.basename(file).strip('.txt') == text_split[1]:
                    target_file = os.path.realpath(file)
            if target_file:
                with open(target_file, 'r') as anif:
                    full_ani = anif.read()
                lines = full_ani.split('\n')
                interval = lines[0]
                msgs = []
                tmp_msg = []
                for line in lines[1:]:
                    if ''.join(line).startswith('[f#]'):
                        line = '[f#]'
                    if line != '[f#]':
                        tmp_msg.append(line)
                    else:
                        msgs.append(tmp_msg)
                        tmp_msg = []
                for i in range(loop):
                    for msg in msgs:
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                ts=timestamp,
                                text='```' + '\n'.join(msg) + '```'
                            )
                        except SlackApiError as e:
                            bot.error(e)
                            
                        time.sleep(float(interval))
            else:
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text="**No animation with that name found!**"
                    )
                except SlackApiError as e:
                    bot.error(e)
                    

def stats(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('stats', **payload)
    if data:
        workspace = client.team_info()['team']['name']
        real_ts = float(timestamp)
        now = float(time.time())
        relay = int(float(now - real_ts) * 1000)
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
                    },
                    {
                        "type": "mrkdwn",
                        "text": ":signal_strength: *Response Time:* {}ms".format(relay)
                    }
                ]
            }
        ]
        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text="",
                attachments=[{
                    'color': '#0f87ff',
                    'blocks': blocks
                }]
            )
        except SlackApiError as e:
            bot.error(e)

def customrscmd(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('customrs', **payload)
    if data:
        if len(text_split) < 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="Missing Arguments. Check the wiki for more information.",
                    ts=timestamp
                )
                bot.warning_count += 1
            except SlackApiError as e:
                bot.error(e)
                
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
                        bot.error(e)
                        
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
                        bot.error(e)
                        
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
                        bot.error(e)
                        
                else:
                    num = text_split[2]
                    try:
                        customrs.delete(num)
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="Deleted Custom Reply.",
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            bot.error(e)
                    except IndexError as e:
                        try:
                            web_client.chat_update(
                                channel=channel_id,
                                text="No Custom Reply with That ID",
                                ts=timestamp
                            )
                        except SlackApiError as e:
                            bot.error(e)             
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
                        bot.error(e)
                        
                else:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="No Custom Replies Set! Add some to your config or use the customrs command.",
                            ts=timestamp
                        )
                    except SlackApiError as e:
                        bot.error(e)
                        

def customrsd(**payload):
    bot.message_count += 1
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data.get('ts')
    text = data.get('text')
    if text:
        if user != config['user']:
            if not config['prefix'] in text:
                for custom_reply in customrs.custom_replies:
                    if not custom_reply['is_strict']:
                        if custom_reply['trigger'].lower() in text.lower():
                            try:
                                client.chat_postMessage(
                                    channel=channel_id,
                                    text=custom_reply['reply'],
                                    as_user=True,
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                bot.error(e)
                                
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
                                bot.error(e)
                                
    
def ascii(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('ascii', **payload)
    if data:
        if len(text_split) < 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="You need to feed a string to asciify!",
                    ts=timestamp
                )
            except SlackApiError as e:
                bot.error(e)
                
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
                bot.error(e)
                

def status(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('status', **payload)
    if data:
        if len(text_split) < 3:
            print(Prefixes.warning + 'Missing Arguments! Read Help For Information')
            bot.warning_count += 1
        else:
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
                bot.error(e)
                
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="Failed to set status.",
                        ts=timestamp
                    )
                except SlackApiError as e:
                    bot.error(e)
                    

def setprefix(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('setprefix', **payload)
    if data:
        if len(text_split) != 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="Please only feed one argument for your prefix. You can repeat special chars to act as a longer prefix.",
                    ts=timestamp
                )
            except SlackApiError as e:
                bot.error(e)
                
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
                bot.error(e)
                        

def shelp(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('help', **payload)
    if data:
        attachments = [
            {
                "color": "#0f87ff",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Slacky Help Menu:*"
                        },
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*General*\n`{}help general`\n".format(config['prefix'])
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Fun*\n`{}help fun`\n".format(config['prefix'])
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Info*\n`{}help info`\n".format(config['prefix'])
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Custom Replies*\n`{}help cr`\n".format(config['prefix'])
                            }
                        ]
                    }
                ]
            }]
        attachments_general = [{
            "color": "#d94c63",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*General Commands:*"
                    },
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*ascii*\nConvert String To ASCII Art\n`{}ascii <phrase>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*ani*\nPlay Animation\n`{}ani <name> [loops]`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*delete*\nDelete Last X Messages\n`{}delete <num of msgs>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*howdoi*\nGet Code Snippet From Stack Overflow\n`{}howdoi <query>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*react*\nReact to Last Message\n`{}react <emoji>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*reactrand*\nReact to Last Message with Random Emoji\n`{}reactrand`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*reactspam*\nSpam Last Message with Reactions\n`{}reactspam`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*setstatus*\nSet Your Slack Status\n`{}setstatus <emoji> <status>`\n".format(config['prefix'])
                        }
                    ]
                }
            ]
        }]
        
        attachments_crs = [{
            "color": "#b34cd9",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Custom Reply Commands:*"
                    },
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*customrs add*\nAdd Custom Reply\n`{}customrs add \"<trigger>\" \"<reply>\" [strict|optional]`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*customrs delete*\nDelete Custom Reply\n`{}customrs delete <CR ID>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*customrs list*\nList Custom Replies\n`{}customrs list`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*listener add*\nAdd a Listener\n`{}listener add <trigger>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*listener delete*\nDelete a Listener\n`{}listener delete <trigger>`\n".format(config['prefix'])
                        },
                    ]
                }
            ]
        }]
        attachments_fun = [{
            "color": "#4cd992",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Fun Commands:*"
                    },
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*space*\nAdd a Space In Between Characters\n`{}space <phrase>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*msgstatus*\nEnable/Disable Random Emoji in Status on Msgs\n`{}msgstatus`".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*subspace*\nSubstitute Every Space with an Emoji\n`{}subspace <emoji>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*shift*\nGeNeRaTe ShIfT tExT\n`{}shift <phrase>`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*xkcd*\nGet The Daily xkcd Comic\n`{}xkcd`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*deepfry*\nDeepfry User Image or Image from URL\n`{}deepfry`\n*CUSTOM PLUGIN, MUST LOAD MANUALLY*".format(config['prefix'])
                        }
                    ]
                }
            ]
        }]
        attachments_info = [{
            "color": "#0f874a",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Info Commands:*"
                    },
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*help*\nDisplay Help Menu\n`{}help`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*info*\nDisplay Info About Bot\n`{}info`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*convinfo*\nGet Info About Chat/Channel\n`{}convinfo [#channel]`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*uinfo*\nGet Info About User\n`{}uinfo @user`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*winfo*\nGet Info About Workspace\n`{}winfo`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*stats*\nGet Stats About Bot\n`{}stats`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*ping*\nGet Response Time of Bot\n`{}ping`\n".format(config['prefix'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*listener list*\nList All Listeners\n`{}listener list`\n".format(config['prefix'])
                        }
                    ]
                },
            ]
        }]
        if len(text_split) < 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text='',
                    attachments=attachments
                )
            except SlackApiError as e:
                bot.error(e)
        else:
            if text_split[1] == 'general':
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='',
                        attachments=attachments_general
                    )
                except SlackApiError as e:
                    bot.error(e)
            elif text_split[1] == 'fun':
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='',
                        attachments=attachments_fun
                    )
                except SlackApiError as e:
                    bot.error(e)
            elif text_split[1] == 'crs':
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='',
                        attachments=attachments_crs
                    )
                except SlackApiError as e:
                    bot.error(e)
            elif text_split[1] == 'info':
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='',
                        attachments=attachments_info
                    )
                except SlackApiError as e:
                    bot.error(e)

def reactrand(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('reactrand', **payload)
    if data:
        try:
            web_client.chat_delete(
                channel=channel_id,
                ts=timestamp
            )
        except SlackApiError as e:
            bot.error(e)
            
        conv_info = client.conversations_history(channel=channel_id, count=1)
        latest_ts = conv_info['messages'][0]['ts']
        try:
            web_client.reactions_add(
                channel=channel_id,
                timestamp=latest_ts,
                name=random.choice(emojis)
            )
        except SlackApiError as e:
            bot.error(e)
            

def reactspam(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('reactspam', **payload)
    if data:
        try:
            web_client.chat_delete(
                channel=channel_id,
                ts=timestamp
            )
        except SlackApiError as e:
            bot.error(e)
            
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
                bot.error(e)
                
                        
def ud(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('ud', **payload)
    if data:
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
                bot.error(e)
                        
                        
def space(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('space', **payload)
    if data:
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
                bot.error(e)

def sub_space(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('subspace', **payload)
    if data:
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
                bot.error(e)
                        
                        
def delete(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('delete', **payload)
    if data:
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
                    bot.error(e)
                    
                

def shift(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('shift', **payload)
    if data:
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
                bot.error(e)
                        

def info(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('info', **payload)
    if data:
        try:
            attachment = [
                {
                    "color": "#0f87ff",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": """Running :slack: *Slacky* v{} by <https://twitter.com/maxbridgland|Max Bridgland>
    *Source Code*: <https://github.com/M4cs/Slacky|GitHub>
    *Wiki*: <https://github.com/M4cs/Slacky/wiki|GitHub Wiki>""".format(version, config['prefix'])
                            }
                        }
                    ]
                }
            ]
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text="",
                attachments=attachment
            )
        except SlackApiError as e:
            bot.error(e)
                

def howdoicmd(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('howdoi', **payload)
    if data:
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
            bot.error(e)
            
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
            bot.error(e)
                    

def heartbeat(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('heartbeat', **payload)
    if data:
        try:
            web_client.chat_update(
                channel=channel_id,
                text="I'm Alive!",
                ts=timestamp
            )
        except SlackApiError as e:
            bot.error(e)
                

def react(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('react', **payload)
    if data:
        try:
            web_client.chat_delete(
                channel=channel_id,
                ts=timestamp
            )
        except SlackApiError as e:
            bot.error(e)
            
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
                name=emoji.replace(':', '')
            )
        except SlackApiError as e:
            bot.error(e)
                    

def listenerd(**payload):
    data = payload['data']
    channel_id = data['channel']
    text = data.get('text')
    if bot.msgstatus:
        try:
            client.users_profile_set(
                profile={
                    'status_emoji': ':' + str(random.choice(emojis)) + ':',
                    'status_text': client.users_profile_get(user=config['user'])['profile'].get('status_text'),
                    'status_expiration': 0
                }
            )
        except SlackApiError as e:
            pass
    if text:
        if not config['prefix'] in text:
            if len(listener.listeners) >= 1:
                if any(x in text for x in listener.listeners):
                    print(Prefixes.event + 'Listener Triggered! Message:', text, '| Channel ID:', channel_id)

def listenercmd(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('listener', **payload)
    if data:
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
                    bot.error(e)
                    
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
                    bot.error(e)
                    
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
                    bot.error(e)
                            

def xkcd(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('xkcd', **payload)
    if data:
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
            bot.error(e)

def convinfo(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('convinfo', **payload)
    if data:
        try:
            web_client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text="This may take a while..."
            )
        except SlackApiError as e:
            bot.error(e)
        if len(text_split) == 2:
            if '#' in text_split[1]:
                fsplit = text_split[1].split('|')[0].split('#')[1]
                nsplit = text_split[1].split('|')[1].strip('>')
                print(fsplit)
                bot.command_count += 1
                messages = []
                cursor = ""
                while True:
                    try:
                        hist = client.conversations_history(channel=fsplit, limit=100, cursor=cursor)
                        for i in hist['messages']:
                            messages.append(i)
                        if hist['has_more']:
                            cursor = hist['response_metadata']['next_cursor']
                            pass
                        else:
                            break
                    except SlackApiError as e:
                        bot.error(e)
                lols = 0
                lmaos = 0
                shits = 0
                fucks = 0
                msgs = 0
                for message in messages:
                    msgs += 1
                    if str('lol') in message['text']:
                        lols += 1
                    elif str('lmao') in message['text']:
                        lmaos += 1
                    elif str('shit') in message['text']:
                        shits += 1
                    elif str('fuck') in message['text']:
                        fucks += 1
                    else:
                        pass
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":slack: *Conversation History for  {}:*".format(nsplit.capitalize())
                        }
                    },
                    {
                        'type': 'section',
                        'fields': [
                            {
                                'type': 'mrkdwn',
                                'text': '*# of LOLs:* {}'.format(lols)
                            },
                            {
                                'type': 'mrkdwn',
                                'text': '*# of LMAOs:* {}'.format(lmaos)
                            },
                            {
                                'type': 'mrkdwn',
                                'text': '*# of S--ts:* {}'.format(shits)
                            },
                            {
                                'type': 'mrkdwn',
                                'text': '*# of F--ks:* {}'.format(fucks)
                            },
                            {
                                'type': 'mrkdwn',
                                'text': '*Total Messages:* {}'.format(msgs)
                            }
                        ]
                    }
                ]
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='',
                        attachments=[
                            {
                                'color': '#0f87ff',
                                'blocks': blocks
                            }
                        ]
                    )
                except SlackApiError as e:
                    bot.error(e)
            else:
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text='Error. Bad Channel!'
                    )
                except SlackApiError as e:
                    bot.error(e)
        else:
            bot.command_count += 1
            messages = []
            cursor = ""
            while True:
                try:
                    hist = client.conversations_history(channel=channel_id, limit=100, cursor=cursor)
                    for i in hist['messages']:
                        messages.append(i)
                    if hist['has_more']:
                        cursor = hist['response_metadata']['next_cursor']
                        pass
                    else:
                        break
                except SlackApiError as e:
                    bot.error(e)
            lols = 0
            lmaos = 0
            shits = 0
            fucks = 0
            msgs = 0
            for message in messages:
                msgs += 1
                if str('lol') in message['text']:
                    lols += 1
                elif str('lmao') in message['text']:
                    lmaos += 1
                elif str('shit') in message['text']:
                    shits += 1
                elif str('fuck') in message['text']:
                    fucks += 1
                else:
                    pass
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":slack: *Conversation History:*"
                    }
                },
                {
                    'type': 'section',
                    'fields': [
                        {
                            'type': 'mrkdwn',
                            'text': '*# of LOLs:* {}'.format(lols)
                        },
                        {
                            'type': 'mrkdwn',
                            'text': '*# of LMAOs:* {}'.format(lmaos)
                        },
                        {
                            'type': 'mrkdwn',
                            'text': '*# of S--ts:* {}'.format(shits)
                        },
                        {
                            'type': 'mrkdwn',
                            'text': '*# of F--ks:* {}'.format(fucks)
                        },
                        {
                            'type': 'mrkdwn',
                            'text': '*Total Messages:* {}'.format(msgs)
                        }
                    ]
                }
            ]
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    attachments=[{
                        'color': '#0f87ff',
                        'blocks': blocks
                    }]
                )
            except SlackApiError as e:
                bot.error(e)