from discord.ext.commands import BadArgument


class Panel:
    def __init__(self, name, pid):
        self.name = name
        self.id = pid

    @classmethod
    async def convert(cls, ctx, argument):
        panel_name = argument.casefold().replace(" ", "_")
        if panel_id := (await ctx.cog.config.panels()).get(argument.casefold().replace(" ", "_")):
            return cls(panel_name, panel_id)
        raise BadArgument


async def find_panel(panels: dict, pid: int):
    """Find panel from dict by id
    (find in dict by value)"""
    for panel in panels:
        if panel["id"] == pid:
            return panel
