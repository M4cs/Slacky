import slack

def authenticate(config):
    try:
        client = slack.WebClient(token=config['token'])
        return client
    except:
        return None