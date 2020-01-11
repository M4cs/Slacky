# Slacky
The First Python Selfbot for Slack Workspaces

<p align="center">
  <center><img src="https://github.com/M4cs/Slacky/blob/master/banner.png"></center>
</p>

## What is this?

Slacky was created as way to automate and make Slack more fun to use. It comes with many commands by default and even allows for custom plugins to be built and imported easily.

Slack as far as I can see have no rules against using selfbots so the only people who would probably find this annoying/against policy would be your organizer admistrators.

<p align="center">
  <center><img src="https://github.com/M4cs/Slacky/blob/master/example.gif"></center>
</p>

**Plugin Packs:**

While there are non yet, if and when people end up making plugin packs, they will be displayed here. If you make one please make a PR to the README with a link to your plugin pack's repo!

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

## Default Commands

These will be improved over time

| Command   | Description                            | Usage                         |
| :--: | :--: | :--: |
| heartbeat | Check if bot is up or not              | ~heartbeat                    |
| info      | Get info about the bot                 | ~info                         |
| ascii     | Generate ASCII art from a phrase       | ~ascii msg |
| shift     | CrEaTe ShIfT tExT lIkE tHiS            | ~shift phrase               |
| subspace  | Replace spaces with emojis             | ~subspace :emoji: msg       |
| xkcd      | Get Daily xkcd comic                   | ~xkcd                         |
| react     | React to last sent message             | ~react :emoji:                |
| reactrand | React to with random emoji             | ~reactrand                    |
| reactspam | Spam 23 Reactions (Notification Spam)  | ~randspam                     |
| howdoi    | Find code snippets from stack overflow | ~howdoi loop over list python |
| listener      | Add or remove listeners                | ~listener add/delete phrase |
| listener list | List all listener words                | ~listener list                  |
| help      | Display this message                   | ~help                         |

## Contributing

Contributions can be done through Pull Requests or by creating a plugin pack.

## License

I ask that if you fork this do not release as your own. Please credit and mention it's built off this. In fact building a plugin pack rather than a new bot entirely would be best! The license is MIT so I won't stop you but I'm just asking that you respect my wishes :smile: