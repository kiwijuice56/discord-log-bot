import discord
from discord.ext import commands

# Channel for the bot to post logs to
CHANNEL_ID = 000000000000000000

TOKEN = open("token.txt", "r").readline()
INTENTS = discord.Intents().all()
bot = commands.Bot(command_prefix='%', intents=INTENTS)

# List of words for the bot to delete
banned_words = ["tangy"]


# Initialization of discord bot and ai
@bot.event
async def on_ready() -> None:
    print("Logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="member joined",
        description="*{0}*".format(str(member)),
        color=0x47ff88
    )
    embed.set_thumbnail(url=member.avatar_url)
    await logging_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="member left",
        description="*{0}*".format(str(member)),
        color=0xff0f0f
    )
    embed.set_thumbnail(url=member.avatar_url)
    await logging_channel.send(embed=embed)


@bot.event
async def on_user_update(before, after):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="new profile",
        description="*{0}* to *{1}*".format(str(before), str(after)),
        color=0xa061ff
    )
    embed.set_image(url=after.avatar_url)
    await logging_channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="deletion",
        description=
        "*{0}*'s message in *#{1}* was deleted```{2}\n{3}```".format(
            str(message.author),
            str(message.channel),
            message.created_at,
            message.content),
        color=0xff0f67
    )
    if len(message.attachments) > 0:
        embed.set_image(url=message.attachments[0])
    await logging_channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="edit",
        description="*{0}*'s message in *#{1}* was edited from \n```{2}\n{3}``` to \n```{4}\n{5}```".format(
            str(before.author),
            str(before.channel),
            before.created_at,
            before.content,
            after.edited_at,
            after.content),
        color=0x4dc1ff
    )
    if len(after.attachments) > 0:
        embed.set_image(url=after.attachments[0])
    await logging_channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    contained_banned_words = False
    for word in banned_words:
        if not message.content.lower().find(word) == -1:
            await message.channel.send("message contained banned word: {0}".format(word))
            contained_banned_words = True

    if contained_banned_words:
        await message.delete()


bot.run(TOKEN)
