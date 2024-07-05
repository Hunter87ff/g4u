import discord
import wavelink
from wavelink.ext import spotify
from time import gmtime
from time import strftime
from discord.ui import Button, View
from discord import ButtonStyle
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from modules import config
import typing   




def get_img(search):
    if " " in search:
        search = search.replace(" ", "+")
    word = f"{search}+youtube"
    url = f'https://www.google.com/search?q={word}&tbm=isch'.format(word)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'html')
    images = soup.findAll('img')
    for image in images:
        img_url = image.get('src')
        if "https" in str(img_url):
        	return img_url

cmd = commands
class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot







	@commands.Cog.listener()
	async def on_wavelink_track_end(self, player: wavelink.Player, track: typing.Union[wavelink.YouTubeTrack, spotify.SpotifyTrack, wavelink.SoundCloudTrack, wavelink.YouTubeMusicTrack] , reason):

	    try:
	        ctx = player.ctx
	        vc: player = ctx.voice_client
	        
	    except discord.HTTPException:
	        interaction = player.interaction
	        vc: player = interaction.guild.voice_client
	    
	    if vc.loop:
	        return await vc.play(track)
	    
	    if vc.queue.is_empty:
	        return
	        #return await vc.disconnect()

	    next_song = vc.queue.get()
	    image_url = get_img(search=next_song.title)
	    await vc.play(next_song)
	    tm = "%H:%M:%S"
	    if next_song.duration < 3599:
	        tm = "%M:%S"
	    next_song_emb = discord.Embed(title="<a:music_disk:1020370054665207888>   Now Playing", color=0x303136, description=f'**[{ next_song.title}](https://discord.com/oauth2/authorize?client_id=931202912888164474&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FvMnhpAyFZm&response_type=code&scope=bot%20identify)**\nDuration : {strftime(tm, gmtime(next_song.duration))}\n').set_thumbnail(url=image_url)
	    try:
	        await ctx.send(embed=next_song_emb)

	    except discord.HTTPException:
	        await interaction.send(embed=next_song_emb)



	@cmd.hybrid_command(with_app_command=True)
	async def loop(self, ctx:commands.Context):
		await ctx.defer()
		if ctx.author.voice != None:
			if ctx.voice_client != None:
				vc: wavelink.Player = ctx.voice_client
				if vc.is_playing == False:
					return await ctx.reply(embed=discord.Embed(description="No Audio Available For Loop...", color=0xff0000))
				else:
					vc.loop = True
					await ctx.message.add_reaction(config.vf)

		if ctx.author.voice == None:
			em = discord.Embed(description="Please Join A Voice Channel To Use This Command", color=0xff0000)
			await ctx.reply(embed=em)

		if ctx.voice_client == None:
			return await ctx.reply(embed=discord.Embed(description="I'm Not Connected To Vc!!"))





#, wavelink.SoundCloudTrack
	@cmd.command(aliases= ['p','P'])
	async def play(self, ctx:commands.Context, *, search: typing.Union[wavelink.YouTubeTrack, spotify.SpotifyTrack, wavelink.SoundCloudTrack, wavelink.YouTubeMusicTrack]):
		if ctx.author.bot:
			return
		next_btn = Button(emoji="<:Skip:1019218793597243462>", custom_id="next_btn")
		pause_btn = Button(emoji="<:Pause:1019217055712559195>", custom_id="pause_btn")
		stop_btn = Button(emoji="<:WhiteButton:1019218566475681863>", style=ButtonStyle.danger, custom_id="stop_btn")
		queue_btn = Button(emoji="<:_playlist:1019219174070951967>", style=ButtonStyle.blurple, custom_id="queue_btn")
		play_btn = Button(emoji="<:play_btn:1019504469299441674>", custom_id="play_btn")

		btns = [next_btn, pause_btn, play_btn, stop_btn, queue_btn]
		view = View()
		for btn in btns:
		    view.add_item(btn)

		if ctx.author.bot:
			return


		if not ctx.author.voice:
			return await ctx.send("Please Join a vc")



		if ctx.voice_client is not None:
			if ctx.author.voice is not None:
				if ctx.voice_client.channel != ctx.author.voice.channel:
					await ctx.voice_client.disconnect()
					vc: wavelink.Player = await ctx.author.voice.channel.connect(self_deaf=True, reconnect=True, cls=wavelink.Player)
					
					
				if ctx.voice_client.channel == ctx.author.voice.channel:
					vc: wavelink.Player = ctx.voice_client


		if not ctx.voice_client:
			try:
				vc: wavelink.Player = await ctx.author.voice.channel.connect(self_deaf=True, reconnect=True, cls=wavelink.Player)#reconnect=True, self_deaf=True,
			except:
				return await ctx.send("Please Join a vc")




		if vc.queue.is_empty and not vc.is_playing():
		    await vc.play(search)
		    tm = "%H:%M:%S"
		    if search.duration < 3599:
		        tm = "%M:%S"
		    image_url = get_img(search=search.title)
		    em = discord.Embed(title="<a:music_disk:1020370054665207888>   Now Playing", color=0x303136, description=f'**[{search.title}](https://discord.com/oauth2/authorize?client_id=931202912888164474&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FvMnhpAyFZm&response_type=code&scope=bot%20identify)**\nDuration : {strftime(tm, gmtime(search.duration))}\n').set_thumbnail(url=image_url)
		    await ctx.send(embed=em, view=view)
		            
		else:
		    await vc.queue.put_wait(search)
		    await ctx.send('Added to the queue...', delete_after=5)
		vc.ctx = ctx

		try:
		    if vc.loop: 
		    	return

		except Exception:
		    setattr(vc, "loop", False)




	@cmd.hybrid_command(with_app_command=True)
	async def spotify(self, ctx, spotify_url: str):
		await ctx.defer()
		if not ctx.voice_client:
			await Music.join(self, ctx)
		player: wavelink.Player = ctx.voice_client
		ms = await ctx.send("Playlist Loading")
		async for partial in spotify.SpotifyTrack.iterator(query=spotify_url):
			player.queue.put(partial)
		await ms.edit(content="Playlist Loaded.", delete_after=20)





	@cmd.hybrid_command(with_app_command=True, aliases= ['next'])
	async def skip(self, ctx):
		await ctx.defer()
		if not ctx.author.voice:
			return await ctx.reply(embed=discord.Embed(description="Please Join VC To Use This Command", color=0xff0000))
		if ctx.voice_client != None:
			vc: wavelink.Player = ctx.voice_client
		if vc.queue.is_empty:
			return await ctx.send("the queue is empty", ephemeral=True)
		else:
			vc.loop = False
			await vc.stop()





	@cmd.hybrid_command(with_app_command=True)
	async def pause(self, ctx):
	    await ctx.defer()
	    if not ctx.author.voice:
	        return await ctx.reply("Please Join VC")

	    if ctx.voice_client != None:
	        vc : wavelink.Player = ctx.voice_client


	        if vc.is_playing:
	            await vc.pause()


	@cmd.hybrid_command(with_app_command=True)
	async def resume(self, ctx):
	    await ctx.defer()
	    if not ctx.author.voice:
	        return await ctx.reply("Please Join VC")

	    if ctx.voice_client != None:
	        vc : wavelink.Player = ctx.voice_client


	        if vc.is_paused:
	            await vc.resume()


	@cmd.hybrid_command(with_app_command=True)
	async def queue(self, ctx):
	    await ctx.defer()
	    if not ctx.voice_client:
	        return await ctx.send("im not even in a vc...")

	    elif not getattr(ctx.author.voice, "channel", None):
	        return await ctx.send("join a voice channel first lol")


	    vc: wavelink.Player = ctx.voice_client
	    if vc.queue.is_empty:
	        return await ctx.send("the queue is empty")
	    em = discord.Embed(title="Queue", color=0x303136)
	    
	    queue = vc.queue.copy()
	    songCount = 0
	    for song in queue:
	        songCount += 1
	        em.add_field(name=f"Song Position {str(songCount)}", value=f"`{song}`")
	    await ctx.send(embed=em)






	@cmd.Cog.listener()
	async def on_interaction(self, interaction):
		if "custom_id" not in interaction.data:
			return
		if interaction.message:
			ctx = await self.bot.get_context(interaction.message)

		if interaction.data["custom_id"] == "stop_btn":
			if not interaction.user.voice:
				return await interaction.response.send_message("Please Join VC", ephemeral=True)
			if ctx.voice_client != None:
				try:
					await ctx.voice_client.disconnect()
					await interaction.response.send_message("Successfully Disconnected", ephemeral=True)
					await interaction.message.delete()
				except:
					pass



		if interaction.data["custom_id"] == "next_btn":
			if not interaction.user.voice:
				return await interaction.response.send_message("Please Join VC", ephemeral=True)

			if ctx.voice_client != None:
				vc: wavelink.Player = ctx.voice_client
				#player = bot.wavelink.get_player(ctx.guild.id)

			if vc.queue.is_empty:
				return await interaction.response.send_message("the queue is empty", ephemeral=True)

			else:
			    ms = await interaction.response.send_message("Skiping...", ephemeral=True)
			    vc.loop = False
			    await vc.stop()




		if interaction.data["custom_id"] == "queue_btn":
		    if not interaction.user.voice:
		        return await interaction.response.send_message("Please Join VC", ephemeral=True)

		    vc: wavelink.Player = ctx.voice_client
		    if vc.queue.is_empty:
		        return await interaction.response.send_message("Queue is empty", ephemeral=True)
		    em = discord.Embed(title="Queue", color=0x303136)
		    
		    queue = vc.queue.copy()
		    songCount = 0
		    for song in queue:
		        songCount += 1
		        em.add_field(name=f"Song Position {str(songCount)}", value=f"`{song}`")
		    await interaction.response.send_message(embed=em, ephemeral=True)
		    
		    
		if interaction.data["custom_id"] == "pause_btn":
		    if not interaction.user.voice:
		        return await interaction.response.send_message("Please Join VC", ephemeral=True)
		        
		    if ctx.voice_client != None:
		        vc : wavelink.Player = ctx.voice_client

		        if vc.is_playing:
		            vc.pause()
		            return await interaction.response.send_message("Paused", ephemeral=True)


		if interaction.data["custom_id"] == "play_btn":
		    if not interaction.user.voice:
		        return await interaction.response.send_message("Please Join VC", ephemeral=True)
		        
		    if ctx.voice_client != None:
		        vc : wavelink.Player = ctx.voice_client

		        if vc.is_paused:
		            vc.resume()
		            return await interaction.response.send_message("Resumed", ephemeral=True)



	@cmd.hybrid_command(with_app_command=True, aliases= ['connect'])
	async def join(self, ctx:commands.Context):
		await ctx.defer()
		if not ctx.author.voice:return await ctx.reply("Please Join VC")
		if not ctx.voice_client:
			try:
				await ctx.author.voice.channel.connect(self_deaf=True, reconnect=True, cls = wavelink.Player)
				await ctx.author.voice.channel.connect()
			except:return await ctx.reply("Please Join VC")
		if ctx.voice_client != None:
		  try:await ctx.voice_client.move_to(ctx.author.voice.channel)
		  except:return



	@cmd.hybrid_command(with_app_command=True, aliases= ["stop", "disconnect", "Stop"])
	async def leave(self, ctx):
		await ctx.defer()
		if ctx.author.voice == None:
			return await ctx.reply("Please Join VC")

		if ctx.voice_client:
			return await ctx.voice_client.disconnect()

		if not ctx.voice_client:
			return await ctx.reply("I'm Not Connected To Vc")






async def setup(bot):
    await bot.add_cog(Music(bot))