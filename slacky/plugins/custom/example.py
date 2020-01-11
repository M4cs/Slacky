from slacky import client, config, Prefixes, check_user
from slack.errors import SlackApiError

def custom_example(**payload):
    # Get Data from Payload
    data = payload['data']
    channel_id = data['channel'] # Get Channel ID
    user = data.get('user') # Get User
    timestamp = data['ts'] # Get msg Timestamp
    if check_user(user): # Check if User == You
        web_client = client # Init Client
        text = data.get('text') # Get Text
        # Check for Command Here
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == config['prefix'] + 'example':
                # Command has been triggered
                print(Prefixes.event + 'Ran Command: example')
                # Do your logic here and then update the message at the end below.
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        ts=timestamp,
                        text="This command is an example custom command."
                    )
                except SlackApiError as e:
                    print(Prefixes.error + str(e))