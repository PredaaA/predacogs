from .grafana import Grafana


def setup(bot):
    bot.add_cog(Grafana(bot))
