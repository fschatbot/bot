import discord, traceback
from discord.ext import commands
from util import utils # Your IDE will throw an error, ignore it, it's being dumb. Everything will be fine as long as you run bot.py from the directory it is in.


class Moderation(commands.Cog):
	"""Moderation Cog"""

	def __init__(self, client):
		self.client = client
		self.devs = [252104964753719296, 573986854366347274]


	@commands.command(aliases=["bean", "bonk"])
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		await member.ban(reason=reason)
		await ctx.send(":white_check_mark: Successfully banned user")

	@commands.command(aliases=["boot"])
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		await member.kick(reason=reason)
		await ctx.send(":white_check_mark: Successfully kicked user")


	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def brokenban(self, ctx, *args):
		"""WIP"""
		allowed = False
		if p := utils.admin_dash_o(ctx, args, 2):
			allowed = True
		if p == 2:
			args = args[1:]
		if allowed:
			bans = {"Success": [], "Forbidden": [], "Failed": []}
			for x in await utils.get_users(self.client, args):
				if isinstance(x, str):
					bans["Failed"].append(x + " (already banned or doesn't exist)")
					continue

				if x.id in self.devs:
					bans["Forbidden"].append(x.mention)
					continue

				try:
					await ctx.guild.ban(x)

				except discord.Forbidden:
					bans["Forbidden"].append(x.mention)

				except discord.HTTPException:
					bans["Failed"].append(x.mention)

				except Exception as e:
					await ctx.send(f"An unknown error occurred while attempting to ban {x.mention}:\n{e}")
					traceback.print_exc()

				else:
					bans["Success"].append(x)

			await ctx.send("Output:")
			for y in bans.keys():  # NOW THIS IS COMPACTNESS
				await ctx.send("\n".join([f"{y}:"] + bans[y])) if bans[y] else 0

	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(kick_members=True)
	async def brokenkick(self, ctx, *member):
		"""WIP"""
		allowed = False
		if p := utils.admin_dash_o(ctx, member, 1):
			allowed = True
		if p == 2:
			member = member[1:]
		if allowed:
			kicks = {"Success": [], "Forbidden": [], "Failed": []}
			for x in await utils.get_users(self.client, member):
				if isinstance(x, str):
					kicks["Failed"].append(x + " (not in server or doesn't exist)")
					continue

				if x.id in self.devs:
					kicks["Forbidden"].append(x.mention)
					continue

				try:
					await ctx.guild.kick(x)

				except discord.Forbidden:
					kicks["Forbidden"].append(x.mention)

				except discord.HTTPException:
					kicks["Failed"].append(x.mention)
				except Exception as e:
					await ctx.send(f"An unknown error occurred while attempting to kick {x.mention}:\n{e}")
					traceback.print_exc()

				else:
					kicks["Success"].append(x)

			await ctx.send("Output:")
			for y in kicks.keys():  # NOW THIS IS COMPACTNESS
				await ctx.send("\n".join([f"{y}:"] + kicks[y])) if kicks[y] else 0

	@commands.command()
	@commands.bot_has_permissions(manage_roles=True)
	async def mute(self, ctx, *args):
		allowed = False
		if p := utils.admin_dash_o(ctx, args, 0):
			allowed = True
		if p == 2:
			args = args[1:]
		if allowed:
			mutes = {"Success": [], "Forbidden": [], "Failed": []}
			for x in await utils.get_users(self.client, args):
				if isinstance(x, str):
					mutes["Failed"].append(x + " (doesn't exist)")
					continue

				if x.id in self.devs:
					mutes["Forbidden"].append(x.mention)
					continue

				try:
					await ctx.guild.get_member(x.id).add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))

				except discord.Forbidden:
					mutes["Forbidden"].append(x.mention)

				except discord.HTTPException:
					mutes["Failed"].append(x.mention)

				except Exception as e:
					await ctx.send(f"An unknown error occurred while attempting to mute {x.mention}:\n{e}")
					traceback.print_exc()

				else:
					mutes["Success"].append(x)

			await ctx.send("Output:")
			for y in mutes.keys():  # NOW THIS IS COMPACTNESS
				await ctx.send("\n".join([f"{y}:"] + mutes[y])) if mutes[y] else 0

	@commands.command()
	@commands.bot_has_permissions(manage_roles=True)
	async def unmute(self, ctx, *args):
		allowed = False
		if p := utils.admin_dash_o(ctx, args, 0):
			allowed = True
		if p == 2:
			args = args[1:]
		if allowed:
			unmutes = {"Success": [], "Forbidden": [], "Failed": []}
			for x in await utils.get_users(self.client, args):
				if isinstance(x, str):
					unmutes["Failed"].append(x + " (doesn't exist)")
					continue

				if x.id in self.devs:
					unmutes["Forbidden"].append(x.mention)
					continue

				try:
					await ctx.guild.get_member(x.id).remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))

				except discord.Forbidden:
					unmutes["Forbidden"].append(x.mention)

				except discord.HTTPException:
					unmutes["Failed"].append(x.mention)

				except Exception as e:
					await ctx.send(f"An unknown error occurred while attempting to unmute {x.mention}:\n{e}")
					traceback.print_exc()

				else:
					unmutes["Success"].append(x)

			await ctx.send("Output:")
			for y in unmutes.keys():  # NOW THIS IS COMPACTNESS
				await ctx.send("\n".join([f"{y}:"] + unmutes[y])) if unmutes[y] else 0


	@commands.command(aliases=['cs'])
	@commands.has_permissions(manage_channels=True)
	async def channelstats(self, ctx): 
		channel = ctx.channel 
		embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=discord.Colour.from_rgb(0, 255, 255))
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author.name}")

		await ctx.send(embed=embed)

	@commands.command(aliases=["w", "wrn",])
	@commands.has_permissions(manage_messages=True)
	async def warn(self, ctx, user_id=None, *, args=None):
		if None not in (user_id, args):
			try:
				target = await self.client.fetch_user(user_id)
				await target.send(f"You were warned in {ctx.guild.name} for {args}")
				await self.client.fetch_user
			except:
				await ctx.send(f"Failed to warn {target.name}")
			else:
				await ctx.send(f":white_check_mark: {target.name} was warned")

		else:
			await ctx.send("You are missing a user/message in your warning")

	@commands.command(hidden=True)
	async def channels(self, ctx):
		x = 1 
		for channel in ctx.guild.channels:
			x+=1
		await ctx.send(f"Total channels: {x}")
				

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, amount: int, silent=None):
		if silent == "--silent":
			await ctx.message.delete()
			await ctx.channel.purge(limit=amount)
		else:
			await ctx.channel.purge(limit=amount + 1)
			await ctx.send(f":white_check_mark: Successfully deleted messages")


def setup(client):
	client.add_cog(Moderation(client))


def teardown(client):
	client.remove_cog(Moderation.__name__)
