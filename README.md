<p align="center">
  <center><img src="https://github.com/M4cs/Slacky/blob/master/banner.png"><br>
</p>


[![GitHub stars](https://img.shields.io/github/stars/M4cs/Slacky)](https://github.com/M4cs/Slacky/stargazers) [![GitHub forks](https://img.shields.io/github/forks/M4cs/Slacky)](https://github.com/M4cs/Slacky/network) [![GitHub license](https://img.shields.io/github/license/M4cs/Slacky)](https://github.com/M4cs/Slacky/blob/master/LICENSE) [![Discord Server](https://img.shields.io/badge/Discord-Join%20For%20Support-blue)](https://discord.gg/JjZwJVF) [![Run on Repl.it](https://repl.it/badge/github/M4cs/Slacky)](https://repl.it/github/M4cs/Slacky)


The First Python Selfbot for Slack Workspaces :star:

## What is this?

Slacky was created as way to automate and make Slack more fun to use. It comes with many commands by default and even allows for custom plugins to be built and imported easily.

Slack as far as I can see have no rules against using selfbots so the only people who would probably find this annoying/against policy would be your organizer admistrators.

Discord for Support: https://discord.gg/JjZwJVF

## This README doesn't have all the info! I've written a readme with a bunch of info on the bot [here](https://github.com/M4cs/Slacky/wiki). Check it out for information on how to Install, Setup, and Customize Slacky!

<p align="center">
  <center><h2 align="center">Slack Client</h2><br><p align="center"><img src="https://github.com/M4cs/Slacky/blob/master/slacky.gif"></p></center>
</p>

<p align="center">
  <center><h2 align="center">Bot Server</h2><br><img src="https://github.com/M4cs/Slacky/blob/master/example.gif"></center>
</p>


## Default Commands

These will be improved over time

| Command   | Description                            | Usage                         |
| :--: | :--: | :--: |
| heartbeat | Check if bot is up or not              | ~heartbeat                    |
| info      | Get info about the bot                 | ~info                         |
| customrs  | Manage custom replies to messages      | [Read Wiki](https://github.com/M4cs/Slacky/wiki) |
| stats     | Get info about the bot running         | ~stats                        |
| ascii     | Generate ASCII art from a phrase       | ~ascii msg |
| shift     | CrEaTe ShIfT tExT lIkE tHiS            | ~shift phrase               |
| subspace  | Replace spaces with emojis             | ~subspace :emoji: msg       |
| space     | Add a space in between each character  | ~space phrase               |
| ani       | Run animation from animation folder    | [Read Wiki](https://github.com/M4cs/Slacky/wiki) |
| ud        | Get urban dictionary definiton         | ~ud query                   |
| setprefix | Sets bot command prefix                | ~setprefix prefix           |
| xkcd      | Get Daily xkcd comic                   | ~xkcd                         |
| delete    | Delete X num of your msgs              | ~delete num_of_msgs           |
| react     | React to last sent message             | ~react :emoji:                |
| reactrand | React to with random emoji             | ~reactrand                    |
| reactspam | Spam 23 Reactions (Notification Spam)  | ~randspam                     |
| howdoi    | Find code snippets from stack overflow | ~howdoi loop over list python |
| listener      | Add or remove listeners                | ~listener add/delete phrase |
| listener list | List all listener words                | ~listener list                  |
| help      | Display this message                   | ~help                         |


## Changelog:

### Update 1.3:

  - Adds `animations` and the `ani` command. Read Wiki for more info on animations.
  - New bots error handling and `errors` command to display errors triggered

### Update 1.2.2:

  - Fix emoji handling in the `react` command

### Update 1.2.1:

  - Fix `customrs` command
  - Regex sucks!

### Update 1.2:

  - Add `stats, space, ud` commands.
  - Clean up more error handling
  - Adds BotMetaData class for bot data like uptime, commands run, errors, etc

### Update 1.1.4:

  - Fix Custom Replies
  - More Error Handling

### Update 1.1.3:

  - Better Error Handling
  - Fix some broken commands

### Update 1.1.2:

  - Clean Up Code a Bit

### Update 1.1.1:

  - Adds Custom Config Creation/Selection Argument
  - Error Handling Updates for Ctrl+C on Config Wizard

### Update 1.1:

  - Adds Custom Replies. Read the [Wiki](https://github.com/M4cs/Slacky/wiki) to learn how to use them.
  - Bug fixes

### Creating Custom Plugins:

Creating custom commands and plugins are easy for Slacky. All plugins are written in Python and you can see an example for yourself in `slacky/plugins/custom/example.py`. To create your own plugin follow these steps:

First, create a file in `slacky/plugins/custom/` with the name of your plugin. This file can hold one or multiple commands, you can also use a folder but that will get more complicated for imports. We will call this file `plugin.py` for now. In this `plugin.py` you will want to follow the format of the current example in the repo for obtaining msg and channel data. Below is the example plugin available already:

**Building Your New Plugin:**

```python
from slacky import client, config, Prefixes
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
```

This plugin simply updates your message to say "This command is an example custom command."

**Installing Your New Plugin:**

Go to `slacky/plugins/custom/__init__.py` and import your plugin(s) inside of it. If you have a plugin inside a file called `plugin.py` you can import it with `from .plugin import *`. This will allow the main plugin fil*e to automatically import your commands.

Now you have to register your command with your RTMClient. To do so go into `slacky/__main__.py` and go to the bottom where you see the example plugin loaded. You can then register your plugin with something like this:

```python
# Function name of command: custom_plugin

@slack.RTMClient.run_on(event='message')
def _custom_plugin(**payload):
    return custom_plugin(**payload)
```

Now restart the bot and you will have loaded your custom plugin!

## Contributing

Contributions can be done through Pull Requests or by creating a plugin pack.

## License

I ask that if you fork this do not release as your own. Please credit and mention it's built off this. In fact building a plugin pack rather than a new bot entirely would be best! The license is MIT so I won't stop you but I'm just asking that you respect my wishes :smile:
