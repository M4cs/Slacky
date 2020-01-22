from slacky import config, bot, Prefixes
from slacky.plugins import cmd_setup
from slack.errors import SlackApiError
import requests, json, random


print(Prefixes.start + "Loading Shutterstock Plugin...")

def stockpic(**payload):
    data, channel_id, user, timestamp, web_client, text, text_split = cmd_setup('stockpic', **payload)
    if data:
        if config.get('shutterstock_key') and config.get('shutterstock_secret'):
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text="Finding an Image..."
                )
            except SlackApiError as e:
                bot.error(e)
            res = requests.get('https://api.shutterstock.com/v2/images/search?query={}'.format('+'.join(text_split[1:])), auth=requests.auth.HTTPBasicAuth(config['shutterstock_key'], config['shutterstock_secret'])).json()
            images = res['data']
            image_links = []
            for image in images:
                image_links.append(image['assets']['preview']['url'])
            link = random.choice(image_links)
            try:
                web_client.chat_update(
                    channel=channel_id,
                    ts=timestamp,
                    text='',
                    attachments=[
                        {
                            'color': '#0a85f2',
                            'blocks': [
                                {
                                    'type': 'image',
                                    'title': {
                                        'type': 'plain_text',
                                        'text': ' '.join(text_split[1:]),
                                        'emoji': True
                                    },
                                    'image_url': link,
                                    'alt_text': 'Stock Image'
                                }
                            ]
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
                    text="Add `shutterstock_key` and `shutterstock_secret` to config with your credentials!"
                )
            except SlackApiError as e:
                bot.error(e)