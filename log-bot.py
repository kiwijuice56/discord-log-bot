import discord
from discord.ext import commands

import shutil
import requests
import os

# Channel for the bot to post logs to
CHANNEL_ID = 000000000000000000

TOKEN = open("token.txt", "r").readline()
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all())

# Image file extensions that the bot recognizes
image_types = [".png", ".jpg", ".jpeg"]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="member joined",
        description=f"*{member}*",
        color=0x47ff88
    )
    embed.set_author(name=member, icon_url=str(member.avatar_url))
    embed.set_footer(text=f"user ID: {member.id}")
    await logging_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="member left",
        description="*{member}*",
        color=0xff0f0f
    )
    embed.set_author(name=member, icon_url=str(member.avatar_url))
    embed.set_footer(text=f"user ID: {member.id}")
    await logging_channel.send(embed=embed)


@bot.event
async def on_user_update(before, after):
    logging_channel = bot.get_channel(CHANNEL_ID)

    embed = discord.Embed(
        title="profile update",
        color=0xa061ff
    )
    embed.set_author(name=before, icon_url=str(before.avatar_url))
    embed.set_footer(text=f"user ID: {after.id}")

    # Currently only checks if the change is either profile picture or username
    if not str(before) == str(after):
        embed.description = f"username changed from *{before}* to *{after}*"
        await logging_channel.send(embed=embed)
    elif not after.avatar_url == before.avatar_url:
        # Temporarily download image to send as attachment
        response = requests.get(after.avatar_url, stream=True)
        with open("img.png", "wb") as out_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, out_file)
        file = discord.File("img.png")
        embed.set_image(url=f"attachment://{file.filename}")
        embed.description = "new avatar: "

        await logging_channel.send(file=file, embed=embed)
        os.remove("img.png")


@bot.event
async def on_message_delete(message):
    logging_channel = bot.get_channel(CHANNEL_ID)

    # Send main embed
    embed = discord.Embed(
        title="deletion",
        description=(
            f"*#{message.channel}*, {len(message.attachments)} attachment(s)\n"
            f"```{message.created_at}\n"
            f"{message.content}```"),
        color=0xff0f67
    )
    embed.set_author(name=message.author, icon_url=str(message.author.avatar_url))
    embed.set_footer(text=f"ID: {message.id}")
    await logging_channel.send(embed=embed)

    # Send sub-embeds for attachments
    for i, attachment in enumerate(message.attachments):
        file = await attachment.to_file()

        sub_embed = discord.Embed(
            description=f"attachment {i + 1}",
            color=0x484848
        )
        sub_embed.set_footer(text=f"ID: {message.id}")

        # Use discord's embed image feature if applicable for prettier presentation
        if True in [file.filename.endswith(ext) for ext in image_types]:
            sub_embed.set_image(url=f"attachment://{file.filename}")

        await logging_channel.send(file=file, embed=sub_embed)


@bot.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    logging_channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(
        title="edit",
        description=(
            f"*#{before.channel}*, {len(after.attachments)} attachment(s)\n"
            f"before: ```{before.created_at}\n"
            f"{before.content}``` after:"
            f"```{after.edited_at}\n"
            f"{after.content}```"
        ),
        color=0x4dc1ff
    )
    embed.set_author(name=after.author, icon_url=str(after.author.avatar_url))
    embed.set_footer(text=f"ID: {after.id}")
    await logging_channel.send(embed=embed)


bot.run(TOKEN)
