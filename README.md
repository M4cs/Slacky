<p align="center">
  <center><img src="https://github.com/M4cs/Slacky/blob/master/banner.png"><br>
</p>


[![GitHub stars](https://img.shields.io/github/stars/M4cs/Slacky)](https://github.com/M4cs/Slacky/stargazers) [![GitHub forks](https://img.shields.io/github/forks/M4cs/Slacky)](https://github.com/M4cs/Slacky/network) [![GitHub license](https://img.shields.io/github/license/M4cs/Slacky)](https://github.com/M4cs/Slacky/blob/master/LICENSE) [![Discord Server](https://img.shields.io/badge/Discord-Join%20For%20Support-blue)](https://discord.gg/JjZwJVF) [![Run on Repl.it](https://repl.it/badge/github/M4cs/Slacky)](https://repl.it/github/M4cs/Slacky)


The First Python Selfbot for Slack Workspaces :star:

## What is this?

Slacky was created as way to automate and make Slack more fun to use. It comes with many commands by default and even allows for custom plugins to be built and imported easily.

Slack as far as I can see have no rules against using selfbots so the only people who would probably find this annoying/against policy would be your organizer admistrators.

Discord for Support: https://discord.gg/JjZwJVF

### This README doesn't have all the info! I've written a readme with a bunch of info on the bot [here](https://github.com/M4cs/Slacky/wiki). Check it out for information on how to Install, Setup, and Customize Slacky!

### Read how to run the bot in multiple workspaces [here](https://github.com/M4cs/Slacky/wiki/Multiple-Workspaces)

### [View Changelog Here](https://github.com/M4cs/Slacky/blob/master/CHANGELOG.md)

<p align="center">
  <center><h2 align="center">Slack Client</h2><br><p align="center"><img src="https://github.com/M4cs/Slacky/blob/master/slacky.gif"></p></center>
</p>

<p align="center">
  <center><h2 align="center">Bot Server</h2><br><img src="https://github.com/M4cs/Slacky/blob/master/example.gif"></center>
</p>


## Default Commands

Assumes prefix is `~`

| Command   | Description                            | Usage                         |
| :--: | :--: | :--: |
| heartbeat | Check if bot is up or not              | ~heartbeat                    |
| uinfo     | Get info about a user                  | ~uinfo @user                  |
| winfo     | Get info about the current workspace   | ~winfo                        |
| convinfo  | Get info about conversation/channel    | ~convinfo #chantag|optional   |
| info      | Get info about the bot                 | ~info                         |
| errors    | See all errors the bot has encountered | ~errors                       |
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

## Contributing

Contributions can be done through Pull Requests or by creating a plugin pack.

## License

I ask that if you fork this do not release as your own. Please credit and mention it's built off this. In fact building a plugin pack rather than a new bot entirely would be best! The license is MIT so I won't stop you but I'm just asking that you respect my wishes :smile:
