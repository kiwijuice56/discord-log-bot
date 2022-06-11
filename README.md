# discord-general-log-bot
A basic discord bot that can log message edits, deletions, and user updates.
Easily extendable to offer other basic utilities, such as the basic content moderation included
in the script. 

## Usage
In order to use the bot, you must download this repository and run the `log-bot.py` script using your own discord bot 
account.

### 1. Create your own discord [bot](https://discord.com/developers/docs/intro)
Set up your bot and copy the token in Discord's developer portal at Application > (your application) > Bot > Token. 
Paste it into `token.txt`.

### 2. Set the channel ID
The bot will post logs in any challenge specified in the script. To find the ID of the channel you are going to use, 
open discord in `Developer Mode`, then right-click the channel and select `Copy ID`. 
Paste this ID inside the script's `CHANNEL_ID` variable.

### 3. Run the `log-bot.py` script
Using any python3 interpreter, run the `log-bot.py` script. When this script is running, your bot should be online and 
available for use!

## Limitations
In order to make the bot more light-weight, it does not locally store any images (from profile updates or message
deletions). Instead, it sends the content's Discord URL, allowing it to be visible for a period after the
message's deletion. However, these images are regularly deleted and thus are not permanent. If there is an important
image that the logging bot captured, be sure to save it locally on your own machine.
