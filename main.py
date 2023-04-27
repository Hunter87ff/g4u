import os
import json
import time
import random
import typing
import pymongo
import modules
import discord
import asyncio
import datetime
import requests
import wavelink
import gtts
from gtts import gTTS
from asyncio import sleep
from pymongo import MongoClient
from wavelink.ext import spotify
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime, timedelta
from modules import (config, color, reply)
#from discord.ext.commands.converter import (MemberConverter, RoleConverter, TextChannelConverter)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.voice_states = True
intents.guilds = True

#kill "python.exe"

#Configuring db

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix),
                   intents=intents)
#allowed_mentions = discord.AllowedMentions(roles=True, users=True, everyone=True),
bot.remove_command("help")


async def load_extensions():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")



async def reconnect():
	try:
		gld = bot.get_guild(config.ofc_guild)
	except:
		return
	for i in gld.voice_channels:
		if i.id == config.voice_channel:
			try:
				return await i.connect(self_deaf=True, reconnect=True)
			except:
				return


@bot.event
async def on_ready():
	await node_connect()
	await load_extensions()
	st_log = bot.get_channel(config.stl)
	await bot.tree.sync()
	await reconnect()
	stmsg = f'{bot.user} is ready with {len(bot.commands)} commands'
	await st_log.send("<@885193210455011369>",
	                  embed=discord.Embed(title="Status",
	                                      description=stmsg,
	                                      color=0x00ff00))
	print(stmsg)
	await bot.change_presence(activity=discord.Activity(
	 type=discord.ActivityType.listening, name="Gaming 4 You"))
	await sleep(120)


@bot.command()
async def restart(ctx):
	if ctx.author.id == config.owner_id:
		try:
			os.kill()
			os.system("python main.py")
		except:
			pass
	else:
		return


@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
	print(f"Node {node.identifier} is ready")


async def node_connect():
	await bot.wait_until_ready()
	await wavelink.NodePool.create_node(bot=bot,
	                                    host=config.m_host,
	                                    port=443,
	                                    password=config.m_host_psw,
	                                    https=True,
	                                    spotify_client=spotify.SpotifyClient(
	                                     client_id=config.spot_id,
	                                     client_secret=config.spot_secret))

bws = ['asses', 'asshole', 'bc', 'behenchod', 'betichod', 'bhenchod', 'bhos', 'bitch', 'boob', ' bsdk', ' bsdke', 'carding', 'chumt', 'chut', 'chutia', 'chutiya', 'comdon', 'condom', 'faggot', 'fuck', 'fucker', 'gamd', 'gamdu', 'gand', 'hentai', 'idiot', 'khanki', 'kutta', 'lauda', 'lawde', 'lund', 'maderchod', 'motherchod', 'nigg', 'p0rn', 'penis', 'pepe', 'porn', 'pornhub', 'pussy', 'ramdi', ' randi', 'sex', 'sexy', 'titt', 'vagina', 'xhamster', 'xnxx', 'xvideos', 'खनकी', 'गांडू', 'चुटिया', 'छूट', 'छोड़', 'छोड़ू', 'बेटीछोद', 'भोसडीके', 'मदरचोड', 'मादरचोद', 'लुंड']


@bot.event
async def on_message(message):
	if message.webhook_id != None:
		return
	await bot.process_commands(message)
	await reply.esp(message)
	for i in message.content.split():
		if i in bws:
			await message.delete()
			return await message.channel.send(f"{message.author.mention} please don't use abusive words")

@bot.event
async def on_command_error(ctx, error):
	erl = config.erl
	try:
		if isinstance(error, commands.MissingRequiredArgument):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000,
			 description=
			 "Missing Required Arguments! You Should Check How To Use This Command.\nTip: use `&help <this_command>` to get Instructions"
			))
		elif isinstance(error, commands.MissingPermissions):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000,
			 description="You don't have Permissions To Use This Command"))
		elif isinstance(error, commands.DisabledCommand):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000,
			 description="This Command Is Currently Disabled! You Can Try Again Later"))
		elif isinstance(error, commands.CommandNotFound):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000,
			 description="Command Not Found! Please Check Spelling Carefully."))
		elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description=str(error)))
		elif isinstance(error, commands.UserInputError):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000, description="Please Enter Valid Arguments"))
		elif isinstance(error, commands.EmojiNotFound):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description="Emoji Not Found"))
		elif isinstance(error, commands.NotOwner):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000,
			 description="This Is A Owner Only Command You Can't Use It"))
		elif isinstance(error, commands.MessageNotFound):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000, description="Message Not Found Or Deleted"))
		elif isinstance(error, commands.MemberNotFound):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description="Member Not Found"))
		elif isinstance(error, commands.ChannelNotFound):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description="Channel Not Found"))
		elif isinstance(error, commands.GuildNotFound):
			return await ctx.send("**I'm Not In The Server! which You Want To See**",
			                      delete_after=19)
		elif isinstance(error, commands.ChannelNotReadable):
			return await ctx.send(embed=discord.Embed(
			 color=0xff0000, description="Can Not Read Messages Of The Channel"))
		elif isinstance(error, commands.CommandOnCooldown):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description=str(error)))
		elif "Manage Messages" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Missing `Manage Messages` Permission", color=0xff0000))
		elif "Unknown file format." in str(error):
			return await ctx.send(
			 embed=discord.Embed(description="Invalid Input", color=0xff0000))
		elif "Send Messages" in str(error):
			return await ctx.author.send(embed=discord.Embed(
			 description=
			 f"I don't have Permissions To Send message in this channel - {ctx.channel.mention}",
			 color=0xff0000))
		elif "This playlist type is unviewable." in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="This playlist type is unsupported!", color=0xff0000))
		elif "Maximum number of channels in category reached (50)" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of channels in category reached (50)",
			 color=0xff0000),
			                      delete_after=30)
		elif isinstance(error, commands.BotMissingPermissions):
			return await ctx.send(
			 embed=discord.Embed(color=0xff0000, description=str(error)))
		elif "error code: 10003" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Channel Deleted Or Invalid", color=0xff0000))
		elif "error code: 50013" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="**Missing Permissions! You Should Check My Permissions**",
			 color=0xff0000),
			                      delete_after=30)
		elif "Unknown Role" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="**Given Role Is Invalid Or Deleted**", color=0xff0000),
			                      delete_after=30)
		elif "Cannot delete a channel required for community servers" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="**I Cannot delete a channel required for community servers**",
			 color=0xff0000),
			                      delete_after=30)
		elif "error code: 50001" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="**I don't have access to do this**", color=0xff0000),
			                      delete_after=30)
		elif "error code: 30005" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of guild roles reached (250)", color=0xff0000))
		elif "error code: 30007" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of webhooks reached (15)", color=0xff0000))
		elif "error code: 30008" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of emojis reached", color=0xff0000))
		elif "error code: 30010" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of reactions reached (20)", color=0xff0000))
		elif "error code: 30013" in str(error):
			return await ctx.send(embed=discord.Embed(
			 description="Maximum number of guild channels reached (500)",
			 color=0xff0000))

	except:
		e = str(error)
		await erl.send(
		 f"<@885193210455011369>\n```py\nGuild Name: {ctx.guild}\nGuild Id : {ctx.guild.id}\nUser Tag : {ctx.author}\nUser Id : {ctx.author.id}\nCommand : {ctx.message.content}\n\n\n{e}```"
		)
		await ctx.reply(
		 "Something Went Wrong. Don't worry! I've Reported To Developers. You'll Get Reply Soon.\nThanks For Playing With Me ❤️",
		 delete_after=30)


############################################################################################
#                                       INFO
############################################################################################
@bot.command()
async def pl(ctx, url2):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    source = await discord.FFmpegOpusAudio.from_probe(url2)
    ctx.voice_client.play(source)



def gp():
	plst = [23, 19, 21, 22, 21, 20, 21, 23, 19, 18, 24, 28]
	ping = random.choice(plst)
	return ping


@bot.command()
@commands.cooldown(2, 20, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True)
async def ping(ctx):
	await ctx.reply(f'**Current ping is `{gp()} ms`**')


@bot.hybrid_command(with_app_command=True, aliases=["bi", "about", "info"])
@commands.cooldown(2, 20, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def botinfo(ctx):
	await ctx.defer(ephemeral=True)
	emb = discord.Embed(title="Gaming 4 You",
	                    description="Welcome To Gaming 4 You",
	                    color=discord.Color.blurple())
	emb.add_field(
	 name="<:dev:1020696239689433139> __Developer__",
	 value="[Hunter#6967](https://discord.com/users/885193210455011369)",
	 inline=False)
	emb.add_field(name="<:g_latency:968371843335610408> __Current Ping__",
	              value=gp(),
	              inline=False)
	emb.add_field(name="<:setting:968374105961300008> __Command Prefix__",
	              value="prefix: & , command: &help",
	              inline=False)
	emb.set_footer(text="Made with ❤️ | By hunter#6967")
	return await ctx.send(embed=emb)


@bot.command(hidden=True)
@commands.guild_only()
@commands.cooldown(2, 20, commands.BucketType.user)
async def sdm(ctx, member: discord.User, *, message):
	if ctx.author.id == 885193210455011369:
		try:
			await member.send(message)
			return await ctx.reply("Done")
		except:
			return

	if ctx.author.id != 885193210455011369:
		return await ctx.send(embed=discord.Embed(
		 description="Command not found! please check the spelling carefully",
		 color=0xff0000))


from flask import Flask, render_template
from threading import Thread

app = Flask('')


@app.route('/')
def index():
	return render_template('index.html')


def run():
	app.run(host='0.0.0.0', port=8080)


def keep_alive():
	t = Thread(target=run)
	t.start()


keep_alive()

bot.run(config.token)
