# discord-general-log-bot
A basic discord bot that can log message edits, deletions, and user updates.
Easily extendable to offer other basic utilities.

## Usage
In order to use the bot, you must download this repository and run the `log-bot.py` script using your own discord bot 
account.

### 1. Create your own discord [bot](https://discord.com/developers/docs/intro)
Set up your bot and copy the token in Discord's developer portal at Application > (your application) > Bot > Token. 
Paste it into `token.txt`.

### 2. Set the channel ID
The bot will post logs in any channel specified in the script. To find the ID of the channel you are going to use, 
open discord in `Developer Mode`, then right-click the channel and select `Copy ID`. 
Paste this ID inside the `channel.txt` file.

### 3. Run the `log-bot.py` script
Ensure that you have the packages at the top of the `log-bot.py` installed (namely, `requests` and `discord.py`).
Using any python3 interpreter, run the `log-bot.py` script.
When this script is running, your bot should be online and 
available for use!
