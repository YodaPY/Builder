import time
import hikari
import inspect
import textwrap
from vexilux import Command
from lightbulb import Plugin, command
from lightbulb.utils import EmbedNavigator, EmbedPaginator
from builder.bot import BuilderBot, Context, TranslationType, command_converter

class Bot(Plugin):
    """
    Info about the bot and basic commands
    """

    __slots__ = ("bot", )

    def __init__(self, bot: BuilderBot) -> None:
        self.bot = bot

        super().__init__()

    @command(cls=Command)
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

    @command(cls=Command)
    async def source(self, ctx: Context, *, command: command_converter) -> None:
        """
        View the source for a command
        """

        callback = command.callback
        code = textwrap.dedent((inspect.getsource(callback))).replace("\x60", "\u02CB") #so it renders properly

        file_path = inspect.getsourcefile(callback)
        file_ext = file_path.split(".")[-1]
        short_file_path = (file_path.split("Builder"))[1]
        file_path = f"https://github.com/YodaPY/Builder/blob/master{short_file_path}"

        lines, lineno = inspect.getsourcelines(callback)
        line_path = f"L{lineno}-L{lineno + len(lines) - 1}"

        github_path = file_path + "#" + line_path

        paginator = EmbedPaginator(max_lines=20)

        for line in code.splitlines():
            paginator.add_line(line)

        @paginator.embed_factory()
        def _(index: int, content: str) -> hikari.Embed:
            content = f"```{file_ext}\n{content}```"
            embed = hikari.Embed(
                title="Github",
                description=content,
                url=github_path
            )
            embed.set_footer(text=f"Page {index}/{len(paginator)}")

            return embed

        navigator = EmbedNavigator(paginator.build_pages())
        await navigator.run(ctx)
    
def load(bot: BuilderBot) -> None:
    bot.add_plugin(Bot(bot))