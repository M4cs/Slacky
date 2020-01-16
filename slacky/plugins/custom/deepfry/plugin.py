from slacky import client, config, check_user, bot, version, Prefixes
from .deepfrylogic import deepfryy
from slack.errors import SlackApiError
from PIL import Image
from io import BytesIO
import httpx, os

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

def deepfry(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('deepfry', **payload)
    if data:
        if len(text_split) < 2:
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="Missing User to Deepfry!"
                )
            except SlackApiError as e:
                bot.error(e)
        else:
            if 'http' in text_split[1]:
                image = httpx.get(text_split[1].strip('<').strip('>')).content
                img = Image.open(BytesIO(image))
                img = deepfryy(img=img, flares=False)
                img.save('./tmp.jpg')
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                    with open('tmp.jpg', 'rb') as imdata:
                        r = httpx.post('https://slack.com/api/files.upload', data={'token': config['token'], 'channels': [channel_id], 'title': 'DEEPFRY', 'as_user': 'True'}, files={'file': imdata})
                    os.remove('tmp.jpg')
                except SlackApiError as e:
                    bot.error(e)
            else:
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
                        url = match['profile'].get('image_512')
                        if url:
                            image = httpx.get(match['profile'].get('image_512')).content
                            img = Image.open(BytesIO(image))
                            img = deepfryy(img=img)
                            img.save('./tmp.jpg')
                            try:
                                web_client.chat_delete(
                                    channel=channel_id,
                                    ts=timestamp
                                )
                                with open('tmp.jpg', 'rb') as imdata:
                                    r = httpx.post('https://slack.com/api/files.upload', data={'token': config['token'], 'channels': [channel_id], 'title': 'DEEPFRY', 'as_user': 'True'}, files={'file': imdata})
                            except SlackApiError as e:
                                bot.error(e)