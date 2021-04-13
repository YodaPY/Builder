import hikari
import random
from typing import Union
from vexilux import Command, add_argument
from asyncpg import UniqueViolationError
from lightbulb import Plugin, command, plugins, has_guild_permissions, WrappedArg, guild_only
from builder.bot import BuilderBot, Context, TranslationType, Guild, convert_arg_to_bool

class Configuration(Plugin):
    """
    Configurate the bot's server settings
    """

    __slots__ = ("bot", )

    def __init__(self, bot: BuilderBot) -> None:
        self.bot = bot

        super().__init__()

        self.bot.subscribe(hikari.GuildAvailableEvent, self.maybe_add_settings)
        self.bot.subscribe(hikari.GuildMessageCreateEvent, self.maybe_add_settings)

    async def maybe_add_settings(self, event: Union[hikari.GuildAvailableEvent, hikari.GuildMessageCreateEvent]) -> None:
        """
        Add the settings for a server if that didn't happen already
        """

        await Guild.get_or_create(guild_id=event.guild_id)

    async def remove_settings(self, event: hikari.GuildLeaveEvent) -> None:
        """
        Remove the settings for a server if the bot got kicked/banned
        """

        record = await Guild.get(guild_id=event.guild_id)

        await record.delete()
    
    @add_argument("case_sensitive", ["--case-sensitive", "-c"], converter=convert_arg_to_bool, greedy=True)
    @add_argument("text", ["--text", "-t"], greedy=True)
    @add_argument("random", ["--random", "-R"])
    @add_argument("reset", ["--reset", "-r"])
    @has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
    @guild_only()
    @command(name="prefix", cls=Command)
    async def set_prefix(self, ctx: Context, **flags) -> None:
        """
        Set the prefix for your server

        NOTE: All given flags are parsed in the order they appear in the signature
        """

        record = await Guild.get(guild_id=ctx.guild_id)
        reset = "reset" in flags.keys()
        text = flags.get("text")
        prefix_choices = flags.get("random")
        case_sensitive = flags.get("case_sensitive")

        if (text or reset or prefix_choices or case_sensitive) is None:
            translated_prefix_msg = (await ctx.translate_message(
                TranslationType.Text,
                0
            )).format(record.prefix)
            return await ctx.respond(translated_prefix_msg)

        if reset:
            prefix = "b!"

        if prefix_choices:
            prefix = random.choice(prefix_choices)

        if text:
            prefix = text

        if case_sensitive is not None:
            record.case_sensitive_prefix = case_sensitive
            await record.save()

            translated_prefix_msg = (await ctx.translate_message(
                TranslationType.Text,
                1
            )).format(str(case_sensitive))
            return await ctx.respond(translated_prefix_msg)

        if len(prefix) > 10:
            translated_prefix_msg = await ctx.translate_message(
                TranslationType.Text,
                2
            )
            return await ctx.respond(translated_prefix_msg)

        record.prefix = prefix
        await record.save()

        translated_prefix_msg = (await ctx.translate_message(
            TranslationType.Text,
            3
        )).format(prefix)

        await ctx.respond(translated_prefix_msg)

    @has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
    @guild_only()
    @command(name="language", aliases=["lang"], cls=Command)
    async def set_language(self, ctx: Context, language: str) -> None:
        """
        Set the language for your server
        """

        lang = self.bot.languages.get(language.lower())

        if not lang:
            translated_lang_msg = (await ctx.translate_message(
                TranslationType.Text,
                0
            )).format(language)

            return await ctx.respond(translated_lang_msg)

        record = await Guild.get(guild_id=ctx.guild_id)
        record.lang = lang
        await record.save()

        translated_lang_msg = (await ctx.translate_message(
            TranslationType.Text,
            1
        )).format(lang)

        await ctx.respond(translated_lang_msg)
 
def load(bot: BuilderBot) -> None:
    bot.add_plugin(Configuration(bot))