# discord-general-log-bot
Basic discord bot that can log and offer other basic utilities.

## Usage
You must download this repository and run the `log-bot.py` script using your own discord bot account.

### 1. Create your own discord [bot](https://discord.com/developers/docs/intro)
Set up your bot and copy the token in Discord's developer portal at Application > (your application) > Bot > Token. Paste it into `token.txt`.

### 2. Set the channel ID
The bot will post logs in any challenge specified in the script. To find the ID of the channel you are going to use, open discord in `Developer Mode`, then right-click the channel and select `Copy ID`. Paste this ID inside the script's `CHANNEL_ID` variable.

### 3. Run the `log-bot.py` script
Using any python3 interpreter, run the `log-bot.py` script. When this script is running, your bot should be online and available for use!

## Features
The bot can currently log:
- Deleted messages
- Edited messages
- Members leaving and joining
- Members editing their profile