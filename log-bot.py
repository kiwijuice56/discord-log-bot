import discord
from discord.ext import commands
# Required to download image files and delete them
import shutil
import requests
import os
# Required to search audit logs by date
import datetime

# IDs for the bot to properly send messages, configured by owner
id_dir = os.path.dirname(__file__)
CHANNEL_ID = int(open(os.path.join(id_dir, "channel.txt"), "r").readline())
TOKEN = open(os.path.join(id_dir, "token.txt"), "r").readline()

# Initialization
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all())
logging_channel = None

# Image file extensions that the bot recognizes
image_types = [".png", ".jpg", ".jpeg"]


@bot.event
async def on_ready():
    global logging_channel
    logging_channel = bot.get_channel(CHANNEL_ID)

    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title="User Joined",
        description=f"*{member}*",
        color=0x47ff88
    )
    embed.set_author(name=member, icon_url=str(member.avatar_url))
    embed.set_footer(text=f"User ID: {member.id}")
    await logging_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    embed = discord.Embed(
        title="User Removed",
        description=f"*{member}*",
        color=0xff0f0f
    )
    embed.set_author(name=member, icon_url=str(member.avatar_url))
    embed.set_footer(text=f"User ID: {member.id}")
    await logging_channel.send(embed=embed)


@bot.event
async def on_user_update(before, after):
    embed = discord.Embed(
        title="User Profile Update",
        color=0xa061ff
    )
    embed.set_author(name=before, icon_url=str(before.avatar_url))
    embed.set_footer(text=f"User ID: {after.id}")

    # Currently only checks if the change is either profile picture or username
    if not str(before) == str(after):
        embed.description = f"Username changed from *{before}* to *{after}*"
        await logging_channel.send(embed=embed)
    elif not after.avatar_url == before.avatar_url:
        # Download and temporarily store image to send as attachment
        response = requests.get(after.avatar_url, stream=True)
        with open("img.png", "wb") as out_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, out_file)

        file = discord.File("img.png")
        embed.set_image(url=f"attachment://{file.filename}")
        embed.description = "New avatar: "
        await logging_channel.send(file=file, embed=embed)
        os.remove("img.png")


@bot.event
async def on_message_delete(message):
    # Use audit logs to get message deleter
    delete_by = None
    async for del_message in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        # Messages deleted by senders do not create an audit log entry, so we must filter out old delete log entries
        if del_message.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=2):
            break
        delete_by = del_message.user

    embed = discord.Embed(
        title="Message Deleted",
        description=(
            f"*#{message.channel}*, {len(message.attachments)} attachment(s)\n"
            f"{'Deleter unknown (likely the sender)' if delete_by is None else f'Deleted by *{delete_by}*'}\n"
            f"```{message.created_at}\n"
            f"{message.content}```"),
        color=0xff0f67
    )
    embed.set_author(name=message.author, icon_url=str(message.author.avatar_url))

    embed.set_footer(text=f"{'' if delete_by is None else f'Deleter ID: {delete_by.id}, '}"
                          f"Sender ID: {message.author.id}, Message ID: {message.id}")
    await logging_channel.send(embed=embed)

    # Send sub-embeds for attachments
    for i, attachment in enumerate(message.attachments):
        file = await attachment.to_file()

        sub_embed = discord.Embed(
            description=f"Attachment {i + 1}",
            color=0x484848
        )
        sub_embed.set_footer(text=f"{'' if delete_by is None else f'Deleter ID: {delete_by.id} '}"
                                  f"Sender ID: {message.author.id}, Message ID: {message.id}")

        # Use discord's embed image feature if applicable for prettier presentation
        if True in [file.filename.endswith(ext) for ext in image_types]:
            sub_embed.set_image(url=f"attachment://{file.filename}")

        await logging_channel.send(file=file, embed=sub_embed)


@bot.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    embed = discord.Embed(
        title="Message Edited",
        description=(
            f"*#{before.channel}*, {len(after.attachments)} attachment(s)\n"
            f"Before: ```{before.created_at}\n"
            f"{before.content}``` After:"
            f"```{after.edited_at}\n"
            f"{after.content}```"
        ),
        color=0x4dc1ff
    )
    embed.set_author(name=after.author, icon_url=str(after.author.avatar_url))
    embed.set_footer(text=f"Sender ID: {after.author.id}, Message ID: {after.id}")
    await logging_channel.send(embed=embed)


bot.run(TOKEN)
