from slacky import client, config, Prefixes, check_user, bot
from slack.errors import SlackApiError
from .CustomBinds import custombinds
import re

def bindmd(**payload):
    bot.message_count += 1   # What's this for fam
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
            if cmd == config['prefix'] + 'bind':
                print(Prefixes.event + 'Ran Command: bind')
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
                        bot.error(e)
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
                                bot.error(e)
                                bot.error_count += 1
                        else:
                            ans = re.findall(r'["“‘\'](.*?)[\'’”"]',  text)
                            bindmsg = ans[0]
                            pastemsg = ans[1]
                            bind_info = {
                                'bind_key': bindmsg,
                                'paste': pastemsg,
                            }
                            custombinds.add(bind_info)
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Added Bind. Bind button is \"{}\" and Paste will be \"{}\".".format(bindmsg, pastemsg),
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                bot.error(e)
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
                                bot.error(e)
                                bot.error_count += 1
                        else:
                            num = text_split[2]
                            custombinds.delete(num)
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="Deleted bind.",
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                bot.error(e)
                                bot.error_count += 1
                    elif action == "list":
                        blocks = []
                        if len(custombinds.binds) > 0:
                            for bind_info in custombinds.binds:
                                blocks.append({
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*#*: {}\n*Bind:* {}\n*Paste:* {}\n".format(custombinds.binds.index(bind_info), bind_info['bind_key'], bind_info['paste'])
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
                                bot.error_count += 1
                        else:
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text="No Custom Binds Set! Add some to your config or use the bind command.",
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                bot.error(e)
                                bot.error_count += 1

def paste(**payload):
    bot.message_count += 1   # What's this for fam
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
            if cmd == config['prefix'] + 'ps':
                print(Prefixes.event + 'Ran Command: paste')
                bot.command_count += 1
                if not text_split[1]:
                    try:
                        web_client.chat_update(
                            channel=channel_id,
                            text="Missing Arguments. Check the wiki for more information.",
                            ts=timestamp
                        )
                        bot.warning_count += 1
                    except SlackApiError as e:
                        bot.error(e)
                        bot.error_count += 1
                else:
                    for bind_info in custombinds.binds:
                        if text_split[1].lower() == bind_info['bind_key']:
                            try:
                                web_client.chat_update(
                                    channel=channel_id,
                                    text=bind_info['paste'],
                                    ts=timestamp
                                )
                            except SlackApiError as e:
                                bot.error(e)
                                bot.error_count += 1
                
