# Slacky Setup Guide (2026)

This guide explains how to set up Slacky with modern Slack authentication using Socket Mode. This approach uses a Slack App for listening to events while sending messages as your personal account.

## Why This Approach?

Slack deprecated legacy tokens and RTM API access for new apps. The modern solution uses:
- **Socket Mode** (via Slack App) - for real-time event listening
- **Browser Session Tokens** (`xoxc-`) - for sending messages as yourself

This hybrid approach lets you:
- Receive commands in real-time
- Send responses that appear as coming from YOUR account (not a bot)

## Prerequisites

- Python 3.7+
- A Slack workspace where you have admin/owner permissions (or can create apps)
- Access to your browser's Developer Tools

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
pip install slack-bolt
```

## Step 2: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it (e.g., "Slacky Listener") and select your workspace
4. Click **Create App**

### Enable Socket Mode

1. In the left sidebar, click **Socket Mode**
2. Toggle **Enable Socket Mode** to ON
3. Click **Generate** to create an App-Level Token
4. Name it (e.g., "slacky-socket") and add the scope `connections:write`
5. Click **Generate**
6. **Copy the token** (starts with `xapp-`) - you'll need this later

### Configure Event Subscriptions

1. In the left sidebar, click **Event Subscriptions**
2. Toggle **Enable Events** to ON
3. Expand **Subscribe to bot events** and add:
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`
4. Click **Save Changes**

### Add Bot Token Scopes

1. In the left sidebar, click **OAuth & Permissions**
2. Scroll to **Scopes** → **Bot Token Scopes**
3. Add these scopes:
   - `channels:history`
   - `channels:read`
   - `groups:history`
   - `groups:read`
   - `im:history`
   - `im:read`
   - `mpim:history`
   - `mpim:read`

### Install the App

1. Scroll up and click **Install to Workspace**
2. Click **Allow**
3. **Copy the Bot User OAuth Token** (starts with `xoxb-`)

## Step 3: Extract Browser Tokens

You need to extract your personal session tokens from the Slack web app.

### Get the xoxc- Token

1. Open Slack in your browser (e.g., `https://app.slack.com`)
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to the **Network** tab
4. Perform any action in Slack (send a message, switch channels)
5. Click on any API request to `slack.com/api/...`
6. Go to the **Payload** tab
7. Find the `token` field - it starts with `xoxc-`
8. Copy this value

### Get the d Cookie

1. In Developer Tools, go to the **Application** tab (Chrome) or **Storage** tab (Firefox)
2. Expand **Cookies** → your Slack domain
3. Find the cookie named `d`
4. Copy its value (starts with `xoxd-`)

### Get the d-s Cookie

1. In the same cookies list, find `d-s`
2. Copy its value (a numeric timestamp)

### Get Your User ID

1. In Slack, click on your profile picture
2. Click **Profile**
3. Click the **More** button (three dots)
4. Click **Copy member ID**

## Step 4: Create Configuration

Create a `config.json` file in the Slacky root directory:

```json
{
    "token": "xoxc-YOUR-XOXC-TOKEN-HERE",
    "d_cookie": "xoxd-YOUR-D-COOKIE-HERE",
    "d_s_cookie": "YOUR-D-S-COOKIE-HERE",
    "app_token": "xapp-YOUR-APP-TOKEN-HERE",
    "bot_token": "xoxb-YOUR-BOT-TOKEN-HERE",
    "user": "YOUR-USER-ID",
    "prefix": "~",
    "listeners": [],
    "custom_replies": []
}
```

Replace the placeholder values:
- `token`: Your `xoxc-` token from Step 3
- `d_cookie`: Your `d` cookie value (keep the URL encoding with `%2F`, `%3D`, etc.)
- `d_s_cookie`: Your `d-s` cookie value
- `app_token`: The `xapp-` token from Step 2
- `bot_token`: The `xoxb-` token from Step 2
- `user`: Your Slack user ID (starts with `U`)
- `prefix`: Command prefix (default `~`)

## Step 5: Invite the Bot to Channels

Before using commands in a channel, invite your Slack App:

1. Go to the channel where you want to use Slacky
2. Type `/invite @YourAppName`
3. Or: Click the channel name → **Integrations** → **Add apps**

## Step 6: Run Slacky

```bash
python -m slacky
```

You should see:
```
[SLACKY] Welcome to Slacky 2.0.0 | The First Python Self-Bot for Slack!
[INFO] Config Loaded
[INFO] Logged in as yourname@yourworkspace
[EVENT] Running Bot (Socket Mode)...
⚡️ Bolt app is running!
```

## Usage

Type commands in any channel where the bot is invited:

- `~help` - Show available commands
- `~ping` - Test if bot is responsive
- `~stats` - Show bot statistics
- `~ascii <text>` - Generate ASCII art
- `~ud <word>` - Urban Dictionary lookup

See the main README for all available commands.

## Troubleshooting

### "invalid_auth" Error

Your browser tokens may have expired. Re-extract the `xoxc-` token and cookies from your browser.

### Bot Not Responding

1. Make sure the Slack App is invited to the channel
2. Verify your user ID matches the one in config
3. Check that you're using the correct prefix (default: `~`)

### "not_in_channel" Error

The bot app needs to be invited to the channel. Use `/invite @YourAppName`.

### Token Expiration

Browser session tokens (`xoxc-`) can expire. If you get auth errors after some time:
1. Re-open Slack in your browser
2. Re-extract fresh tokens
3. Update your `config.json`

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Slack Workspace                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User types: ~ping                                      │
│       │                                                 │
│       ▼                                                 │
│  ┌─────────────────┐         ┌─────────────────┐        │
│  │   Slack App     │         │   Your Account  │        │
│  │  (Socket Mode)  │         │  (xoxc- token)  │        │
│  │                 │         │                 │        │
│  │  Listens for    │         │  Sends response │        │
│  │  message events │────────▶│  as YOU         │        │
│  │                 │         │                 │        │
│  │  xapp- + xoxb-  │         │  xoxc- + cookie │        │
│  └─────────────────┘         └─────────────────┘        │
│                                                         │
│  Response appears as: "your user: pong!"                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Security Notes

- **Never share your tokens** - They provide full access to your Slack account
- **Store config.json securely** - Add it to `.gitignore`
- **Tokens are session-based** - They expire when you log out of the browser
- **Use at your own risk** - Self-bots may violate Slack's Terms of Service

## Files Modified for Socket Mode

- `slacky/__main__.py` - Rewrote to use slack-bolt Socket Mode
- `slacky/api/auth.py` - Updated to use slack_sdk with cookie support
- `config.json` - Added `app_token`, `bot_token`, `d_cookie`, `d_s_cookie`

## License

MIT License - See LICENSE file
