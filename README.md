# Slacky
The First Python Selfbot for Slack Workspaces

## What is this?

Slacky was created as way to automate and make Slack more fun to use. It comes with many commands by default and even allows for custom plugins to be built and imported easily.

Slack as far as I can see have no rules against using selfbots so the only people who would probably find this annoying/against policy would be your organizer admistrators.

<p align="center">
  <center><img src="https://github.com/M4cs/Slacky/blob/master/example.gif"></center>
</p>

## Getting Started:

**Requirements:**
- Python 3
- Slack
- Internet Connection
- Server or Herokuapp Knowledge for Always on Bot

**Installing:**

```
git clone https://github.com/M4cs/Slacky
cd Slacky/
pip3 install -r requirements.txt
python3 -m slacky
```

**Configuration Setup:**

The bot reads from a config file. This config file will be generated through the wizard if you have not already made one. Below are links for grabbing the information needed for the config:

**Get your legacy token for the bot:** https://api.slack.com/custom-integrations/legacy-tokens

**Get your User ID:** 

<p align="center">
  <center><img src="https://help.workast.com/hc/article_attachments/360042136214/Slack_member_ID.gif" />
</p>

# Current Commands

```
+-----------+----------------------------------------+-------------------------------+
| Command   | Description                            | Usage                         |
+-----------+----------------------------------------+-------------------------------+
| heartbeat | Check if bot is up or not              | ~heartbeat                    |
| info      | Get info about the bot                 | ~info                         |
| shift     | CrEaTe ShIfT tExT lIkE tHiS            | ~shift <phrase>               |
| subspace  | Replace spaces with emojis             | ~subspace :smile: <msg>       |
| xkcd      | Get Daily xkcd comic                   | ~xkcd                         |
| react     | React to last sent message             | ~react :emoji:                |
| reactrand | React to with random emoji             | ~reactrand                    |
| reactspam | Spam 23 Reactions (Notification Spam)  | ~randspam                     |
| howdoi    | Find code snippets from stack overflow | ~howdoi loop over list python |
| help      | Display this message                   | ~help                         |
+-----------+----------------------------------------+-------------------------------+
```
