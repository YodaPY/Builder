import aiohttp
from vexilux import Command, add_argument
from lightbulb import Plugin, command
from builder.bot import BuilderBot, Context, TranslationType

class Trading(Plugin):
    """
    Get started and trade your items
    """

    __slots__ = ("bot", )

    def __init__(self, bot: BuilderBot) -> None:
        self.bot = bot

        super().__init__()

    @add_argument("precision", ["--precision", "-p"], converter=int, greedy=True)
    @command(cls=Command)
    async def math(self, ctx: Context, expression: str, **flags) -> None:
        """
        Calculate your expression
        """
        
        precision = flags.get("precision")

        params = {
            "expr": expression
        }
        if precision:
            params["precision"] = precision

        async with aiohttp.request(
            "GET",
            "http://api.mathjs.org/v4",
            params=params
        ) as resp:
            resp.raise_for_status()
            result = (await resp.read()).decode()

        await ctx.respond(result)

def load(bot: BuilderBot) -> None:
    bot.add_plugin(Trading(bot))