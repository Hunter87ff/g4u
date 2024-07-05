import discord
from asyncio import sleep
from discord.ext import commands
cmd = commands
import datetime
import humanfriendly



class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.counter = 0

	#start commands
	
	@cmd.command()
	@commands.cooldown(2, 20, commands.BucketType.user)
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True, send_messages=True)
	@commands.guild_only()
	async def lock(self, ctx, role: discord.Role=None):
		#await ctx.defer()
		bt = ctx.guild.get_member(self.bot.user.id)
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role
		overwrite = ctx.channel.overwrites_for(role)
		overwrite.update(send_messages=False)
		try:
			await ctx.send(f'**<:vf:947194381172084767> Channel has been locked for `{role.name}`**', delete_after=5)
		except:
			return
		await ctx.channel.set_permissions(role, overwrite=overwrite)
		 


	@cmd.hybrid_command(with_app_command = True)
	@commands.cooldown(2, 20, commands.BucketType.user)
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.bot_has_permissions(manage_roles=True)
	async def unlock(self, ctx, role: discord.Role=None, channel:discord.TextChannel=None):
		await ctx.defer()
		if ctx.author.bot:
			return
		if not channel:
			channel = ctx.channel
		if role == None:
			role = ctx.guild.default_role
		overwrite = channel.overwrites_for(role)
		overwrite.update(send_messages=True)
		await channel.set_permissions(role, overwrite=overwrite)
		try:
			return await ctx.send(f'**<:vf:947194381172084767> {channel.mention} has been unlocked from `{role.name}`**', delete_after=5)
		except:
			return



	@cmd.hybrid_command(with_app_command = True)
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.bot_has_permissions(manage_roles=True)
	async def hide(self, ctx, role: discord.Role=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role
		overwrite = ctx.channel.overwrites_for(role)
		overwrite.update(view_channel=False)
		try:
			return await ctx.send(f'**<:vf:947194381172084767>This channel is hidden from `{role.name}`**')
		except:
			return
		await ctx.channel.set_permissions(role, overwrite=overwrite)
		




	@cmd.hybrid_command(with_app_command = True)
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	async def clear_perms(self, ctx, role: discord.Role=None):
		await ctx.defer()
		bt = ctx.guild.get_member(self.bot.user.id)

		if ctx.author.bot:
			return

		if role == None:
			for role in ctx.guild.roles:
				if role.position < bt.top_role.position:
					await role.edit(permissions=discord.Permissions(permissions=0))
			try:
				return await ctx.send(f'**<:vf:947194381172084767>All Permissions Removed from everyone**')
			except:
				return


		if role != None:
			if role.position < bt.top_role.position:
				await role.edit(permissions=discord.Permissions(permissions=0))
				try:
					return await ctx.send(f'**<:vf:947194381172084767>All Permissions Removed from `{role.name}`**')
				except:
					return



	@cmd.hybrid_command(with_app_command = True)
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	async def unhide(self, ctx, role:discord.Role=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role
		overwrite = ctx.channel.overwrites_for(role)
		overwrite.update(view_channel=True)
		await ctx.channel.set_permissions(role, overwrite=overwrite)
		try:
			return await ctx.send(f'**<:vf:947194381172084767>This channel is visible to `{role.name}`**')
		except:
			return



	@cmd.hybrid_command(with_app_command = True, aliases=["lc"])
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	async def lock_category(self, ctx,category: discord.CategoryChannel, role:discord.Role=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role

		for hchannel in category.channels:
		  overwrite = hchannel.overwrites_for(role)
		  overwrite.update(send_messages=False)
		  await hchannel.set_permissions(role, overwrite=overwrite)

		try:
			await ctx.send(f'**<:vf:947194381172084767>Successfully Locked {category.name} From `{role.name}`**')
		except:
			return
			


	@cmd.hybrid_command(with_app_command = True, aliases=["ulc"])
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	async def unlock_category(self, ctx,category: discord.CategoryChannel, role:discord.Role=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role

		for hchannel in category.channels:
		  overwrite = hchannel.overwrites_for(role)
		  overwrite.update(send_messages=True, add_reactions=True)
		  await hchannel.set_permissions(role, overwrite=overwrite)

		try:
			await ctx.send(f'**<:vf:947194381172084767>Successfully Unlocked {category.name}**')
		except:
			return



	@cmd.hybrid_command(with_app_command = True, aliases=["hc"])
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.bot_has_permissions(manage_roles=True)
	async def hide_category(self, ctx,category: discord.CategoryChannel, role:discord.Role=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role

		
		for hchannel in category.channels:
		  overwrite = hchannel.overwrites_for(role)
		  overwrite.update(view_channel=False)
		  await hchannel.set_permissions(role, overwrite=overwrite)
		em = discord.Embed(description=f'**<:vf:947194381172084767> {category.name} is Hidden from `{role.name}`**', color=0x00ff00)
		try:
			await ctx.send(embed=em)
		except:
			return
			#await sleep(1)



	@cmd.hybrid_command(with_app_command = True, aliases=["uhc"])
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.bot_has_permissions(manage_roles=True)
	async def unhide_category(self, ctx, category: discord.CategoryChannel, role :discord.Role = None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if role == None:
			role = ctx.guild.default_role
			

		
		for uhchannel in category.channels:
		  overwrite = uhchannel.overwrites_for(role)
		  overwrite.update(view_channel=True)
		  await uhchannel.set_permissions(role, overwrite=overwrite)
		em = discord.Embed(description=f'**<:vf:947194381172084767> {category.name} is Visible to `{role.name}`**', color=0x00ff00)
		try:
			await ctx.send(embed=em, delete_after=5)
		except:
			return





	#clear command
	@cmd.hybrid_command(aliases=['purge'], with_app_command = True)
	@commands.has_permissions(manage_messages=True)
	@commands.guild_only()
	@commands.bot_has_permissions(manage_messages=True, send_messages=True)
	@commands.cooldown(2, 20, commands.BucketType.user)
	async def clear(self, ctx, amount:int=None):
		await ctx.defer()

		if ctx.author.bot:
			return

		if amount == None:
			amount = 10

		await ctx.channel.purge(limit=amount)
		return await ctx.send(f'**<:vf:947194381172084767> Successfully cleared {amount} messages**',delete_after=5)
		



	#Mute Command
	@cmd.hybrid_command(with_app_command = True)
	@commands.has_permissions(moderate_members=True)
	@commands.bot_has_permissions(moderate_members=True)
	@commands.guild_only()
	async def unmute(self, ctx, member: discord.Member, *, reason=None):
		await ctx.defer()
		bt = ctx.guild.get_member(self.bot.user.id)
		if reason == None:
			reason = 'No reason provided'
		if not ctx.author.top_role.position > member.top_role.position:
			return await ctx.reply("You Can Not Manage Him")

		if not bt.top_role.position > member.top_role.position:
		    return await ctx.reply("I can't manage him")

		else:
		    time = humanfriendly.parse_timespan("0")
		    await member.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
		    try:
		    	await ctx.send(f"{member} has been unmuted")
		    except:
		    	return	


	@cmd.hybrid_command(with_app_command = True)
	@commands.guild_only()
	@commands.has_permissions(moderate_members=True)
	@commands.bot_has_permissions(moderate_members=True, send_messages=True)
	async def mute(self, ctx, member: discord.Member, time=None, *, reason=None):
		await ctx.defer()
		bt = ctx.guild.get_member(self.bot.user.id)
		if time == None:
			time = "5m"

		if reason == None:
			reason = 'No reason provided'

		if not ctx.author.top_role.position > member.top_role.position:
			try:
				return await ctx.reply("You Can Not Manage Him")
			except:
				return

		if not bt.top_role.position > member.top_role.position:
		    try:
		    	return await ctx.reply("I can't manage him")
		    except:
		    	return

		else:
		    timee = humanfriendly.parse_timespan(time)
		    await member.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(seconds=timee), reason=reason)
		    try:
		    	await ctx.send(f"{member} has been muted for {time}.\nReason: {reason}")
		    except:
		    	return




	@cmd.hybrid_command(with_app_command = True)
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(kick_members=True)
	@commands.guild_only()
	async def kick(self, ctx, member: discord.Member, reason=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if reason == None:
			reason = f"{member} kicked by {ctx.author}"

		if ctx.author.top_role.position < member.top_role.position:
			try:
				return await ctx.send("You don't have enough permission")
			except:
				return

		elif member == ctx.author:
			try:
				return await ctx.send("**You can't kick your self**")
			except:
				return

		elif ctx.guild.me.top_role.position < member.top_role.position:
			try:
				return await ctx.send("**I can't kick him**")
			except:
				return

		else:
			return await ctx.guild.kick(member, reason=reason)
			try:
				return await ctx.send(f"{member} kicked")
			except:
				return


	@cmd.hybrid_command(with_app_command = True)
	@commands.bot_has_permissions(ban_members=True)
	@commands.has_permissions(ban_members=True)
	@commands.guild_only()
	async def ban(self, ctx, member: discord.Member, reason=None):
		await ctx.defer()
		if ctx.author.bot:
			return

		if reason == None:
			reason = f"{member} banned by {ctx.author}"

		if ctx.author.top_role.position < member.top_role.position:
			try:
				return await ctx.send(f"{member}'s role is higher than yours", delete_after=5)
			except:
				return

		elif member == ctx.author:
			try:
				return await ctx.send("**You can't ban your self**", delete_after=5)
			except:
				return

		elif ctx.guild.me.top_role.position < member.top_role.position:
			try:
				return await ctx.send("**I can't ban him**", delete_after=5)
			except:
				return

		else:
			await ctx.guild.ban(member, reason=reason)
			try:
				return await ctx.send(f"{member} banned", delete_after=5)
			except:
				return




async def setup(bot):
    await bot.add_cog(Moderation(bot))
