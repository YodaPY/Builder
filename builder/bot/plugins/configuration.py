import hikari
from typing import Union
from asyncpg import UniqueViolationError
from lightbulb import Plugin, command, listener, has_guild_permissions
from builder.bot import BuilderBot, Context, TranslationType, DEFAULT_PREFIX

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

        try:
            await self.bot.db.execute(
                """
                INSERT INTO guild
                (guild_id, prefix, lang)
                VALUES ($1, $2, $3)
                """,
                event.guild_id, DEFAULT_PREFIX, "en"
            )

        except (UniqueViolationError, AttributeError): #Either the guild already has settings
            pass #or the database client hasn't been initialized yet

    async def remove_settings(self, event: hikari.GuildLeaveEvent) -> None:
        """
        Remove the settings for a server if the bot got kicked/banned
        """

        await self.bot.db.execute(
            """
            DELETE FROM guild
            WHERE guild_id = $1
            """,
            event.guild_id
        )
    
    @has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
    @command(name="prefix")
    async def set_prefix(self, ctx: Context, *, prefix: str) -> None:
        """
        Set the prefix for your server
        """

        if len(prefix) > 10:
            translated_prefix_msg = await ctx.translate_message(
                TranslationType.Text,
                0
            )
            return await ctx.respond(translated_prefix_msg)

        await self.bot.db.execute(
            """
            UPDATE guild
            SET prefix = $1
            WHERE guild_id = $2
            """,
            prefix, ctx.guild_id
        )

        translated_prefix_msg = (await ctx.translate_message(
            TranslationType.Text,
            1
        )).format(prefix)

        await ctx.respond(translated_prefix_msg)

    @has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
    @command(name="language")
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

        await self.bot.db.execute(
            """
            UPDATE guild
            SET lang = $1
            WHERE guild_id = $2
            """,
            lang, ctx.guild_id
        )
        translated_lang_msg = (await ctx.translate_message(
            TranslationType.Text,
            1
        )).format(lang)

        await ctx.respond(translated_lang_msg)
 
def load(bot: BuilderBot) -> None:
    bot.add_plugin(Configuration(bot))