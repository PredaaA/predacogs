import discord
import operator
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class WhoPlays(commands.Cog):
    """
        Look at what games people in the server are playing.
        Rewritten for V3, from https://github.com/AznStevy/Maybe-Useful-Cogs/blob/master/whoplays/whoplays.py
    """

    __author__ = ["Stevy", "Predä"]
    __version__ = "0.5.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    @commands.command(aliases=["whoplay"])
    @commands.guild_only()
    async def whoplays(self, ctx, *, game):
        """Shows a list of all the people playing a game."""
        if len(game) <= 2:
            await ctx.send("You need at least 3 characters.")
            return

        member_list = []
        count_playing = 0
        for member in ctx.guild.members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                member_list.append(member)
                count_playing += 1

        if count_playing == 0:
            await ctx.send("No one is playing that game.")
        else:
            sorted_list = sorted(member_list, key=lambda x: getattr(x, "name").lower())
            playing_game = ""
            for member in sorted_list:
                playing_game += "▸ {} ({})\n".format(member.name, member.activity.name)
            embed_list = []
            in_pg_count = 0

            for page in pagify(playing_game, delims=["\n"], page_length=400):
                in_page = page.count("▸")
                in_pg_count = in_pg_count + in_page
                title = f"These are the people who are playing {game}:\n"
                em = discord.Embed(description=page, colour=ctx.author.colour)
                em.set_footer(text=f"Showing {in_pg_count}/{count_playing}")
                em.set_author(name=title)
                embed_list.append(em)

            if len(embed_list) == 1:
                return await ctx.send(embed=em)
            await menu(ctx, embed_list, DEFAULT_CONTROLS)

    @commands.command()
    @commands.guild_only()
    async def cgames(self, ctx):
        """Shows the currently most played games"""
        freq_list = {}
        for member in ctx.guild.members:
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

            em = discord.Embed(description=msg, colour=ctx.author.colour)
            em.set_author(name="These are the server's most played games at the moment:")
            await ctx.send(embed=em)
