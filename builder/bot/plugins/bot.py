import time
from lightbulb import Plugin, command
from builder.bot import BuilderBot, Context, TranslationType

class Bot(Plugin):
    """
    Info about the bot and basic commands
    """

    __slots__ = ("bot", )

    def __init__(self, bot: BuilderBot) -> None:
        self.bot = bot

        super().__init__()

    @command()
    async def ping(self, ctx: Context) -> None:
        """
        Get the heartbeat and REST API latency of the bot
        """

        translated_msg = await ctx.translate_message(
            TranslationType.Text,
            0
        )
        start = time.perf_counter()
        message = await ctx.respond(translated_msg)

        ack = round((time.perf_counter() - start) * 1000)
        heartbeat = round(self.bot.heartbeat_latency * 1000)
        translated_edited_msg = (await ctx.translate_message(
            TranslationType.Text,
            1
        )).format(heartbeat, ack)

        await message.edit(translated_edited_msg)
    
def load(bot: BuilderBot) -> None:
    bot.add_plugin(Bot(bot))