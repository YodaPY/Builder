import os
import json
import hikari
import logging
from lightbulb import Bot, Command
from datetime import datetime, timezone
from builder.database.client import DBClient
from builder.paths import PLUGINS_PATH, I18N_PATH
from builder.bot.context import *
from builder.bot.i18n import *
from builder.config import DEFAULT_PREFIX

class BuilderBot(Bot):
    __slots__ = ("db", "_start_uptime", "logger")

    def __init__(self, database: DBClient, *args, **kwargs) -> None:
        self.db = database
        self.logger: logging.Logger = logging.getLogger("Builder Bot")
        self._start_uptime: datetime = datetime.now(tz=timezone.utc)

        self.translations = {}
        language_files = [
            f for f in os.listdir(I18N_PATH)
            if f.endswith(".json")
        ]

        for lang_file in language_files:
            with open(I18N_PATH + "/" + lang_file) as f:
                data = json.load(f)
            
            self.translations[lang_file[:-5]] = data #we don't want the '.json' file extension

        self.languages = parse_languages()

        super().__init__(*args, **kwargs)

        self.subscribe(hikari.StartingEvent, self.load_plugins)
        self.subscribe(hikari.StartedEvent, self.db.create_pool)

    async def load_plugins(self, _) -> None: #subscription callbacks have to be async and take one argument (event)
        """
        Load all plugins
        """

        plugins = (
            os.path.join(PLUGINS_PATH, f).replace("/", ".")[:-3]
            for f in os.listdir(PLUGINS_PATH)
            if f.endswith(".py")
        )

        for plugin in plugins:
            self.load_extension(plugin)
            self.logger.info("Loaded %s", plugin)

    def get_context(
        self,
        message: hikari.Message,
        prefix: str,
        invoked_with: str,
        invoked_command: Command
    ) -> Context:
        """
        Provide the custom context class for commands
        """

        return Context(self, message, prefix, invoked_with, invoked_command)

async def get_prefix(bot: BuilderBot, message: hikari.Message) -> str:
    if not message.guild_id:
        return DEFAULT_PREFIX

    prefix = await bot.db.fetchval(
        """
        SELECT prefix
        FROM guild
        WHERE guild_id = $1
        """,
        message.guild_id
    )
    return prefix