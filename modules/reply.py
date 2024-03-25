data = {
	"msg" : "Hmara match kab hoga?",
	"reply":"schedule regarding updates apko schedule wale channel pe mil jai ga"
}

match_l = ["match time", "schedule", "mera match kab hai", "hamara match kab hoga","quarter ka match kab hoga?", "semi kab hoga?"]


async def esp(message):
	if message.author.bot:
		return

	if message.author.guild_permissions.administrator == True:
		return
	for m in match_l:
		if m in message.content:
			for i in message.channel.category.channels:
				if "schedule" in i.name:
					return await message.reply(f"ap ko schedule related updates {i.mention} yaha mil jai ga")
		