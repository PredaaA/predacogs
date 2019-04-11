import discord

from redbot.core import commands

import operator


class WhoPlays(commands.Cog):
    """
        Look at what games people in the server are playing.
        Rewritten for V3, from https://github.com/AznStevy/Maybe-Useful-Cogs/blob/master/whoplays/whoplays.py
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["whoplay"])
    @commands.guild_only()
    async def whoplays(self, ctx, *, game):
        """Shows a list of all the people playing a game."""
        if len(game) <= 2:
            await ctx.send("You need at least 3 characters.")
            return

        user = ctx.author
        guild = ctx.guild
        members = guild.members

        playing_game = ""
        count_playing = 0
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    playing_game += "▸ {} ({})\n".format(member.name, member.activity.name)

        if playing_game == "":
            await ctx.send("No one is playing that game.")
        else:
            msg = playing_game
            em = discord.Embed(description=msg, colour=user.colour)
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)
            text = "These are the people who are playing"
            text += " {}:\n{}".format(game, showing)
            em.set_author(name=text)
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    async def cgames(self, ctx):
        """Shows the currently most played games"""
        user = ctx.author
        guild = ctx.guild
        members = guild.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if member.activity.name not in freq_list:
                freq_list[member.activity.name] = 0
            freq_list[member.activity.name] += 1

        sorted_list = sorted(freq_list.items(), key=operator.itemgetter(1), reverse=True)

        if not freq_list:
            await ctx.send("Surprisingly, no one is playing anything.")
        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += "▸ {}: __{}__\n".format(game, freq_list[game])

            em = discord.Embed(description=msg, colour=user.colour)
            em.set_author(name="These are the server's most played games at the moment:")
            await ctx.send(embed=em)
