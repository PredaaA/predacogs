from redbot.core.i18n import Translator

import aiohttp
from io import BytesIO
from datetime import datetime


_ = Translator("DblTools", __file__)


intro_msg = _(
    "To use that cog, you need a Top.gg token. "
    "And for it, you need to have a bot on this bot list, "
    "otherwise you can't use this cog.\n\n"
)
error_message = _(
    "{}To find your API key:\n"
    "**1.** Login on Top.gg <https://top.gg/login>\n"
    "**2.** Go on your profile <https://top.gg/me>\n"
    "**3.** Click on `Edit` on one of your bot.\n"
    "**4.** Scroll to the bottom of the edit page, in `API Options` section, "
    "then click on `Show token` and copy the token.\n"
    "**5.** Use in DM `[p]set api dbl api_key your_api_key_here`\n"
    "**6.** There you go! You can now use DblTools cog."
)


def check_weekend():
    return True if datetime.today().weekday() in [4, 5, 6] else False


async def download_widget(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        return BytesIO(await resp.read())
