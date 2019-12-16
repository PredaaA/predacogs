from .fivem import FiveM


def setup(bot):
    bot.add_cog(FiveM(bot))
