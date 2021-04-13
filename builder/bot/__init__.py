import os
import yarl
import json
import hikari
import typing
import logging
from vexilux import Bot
from lightbulb import Command
from lightbulb.command_handler import maybe_await
from datetime import datetime, timezone
from builder.database import *
from builder.paths import PLUGINS_PATH, I18N_PATH
from builder.bot.context import *
from builder.bot.i18n import *
from builder.config import *
from builder.bot.utils import *
from cryptography.fernet import Fernet
from tortoise import Tortoise

class BuilderBot(Bot):
    __slots__ = ("_start_uptime", "logger")

    def __init__(self, *args, **kwargs) -> None:
        self.logger: logging.Logger = logging.getLogger("Builder Bot")
        self.fernet: Fernet = Fernet(FERNET_KEY)
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
        self.subscribe(hikari.StartedEvent, self.init_database)

        self.remove_command("help")

    async def _resolve_prefix(self, message: hikari.Message) -> typing.Optional[str]:
        prefixes = await maybe_await(self.get_prefix, self, message)

        if isinstance(prefixes, str):
            prefixes = [prefixes]

        prefix = None
        record = await Guild.get(guild_id=message.guild_id)

        for p in prefixes:
            if record.case_sensitive_prefix is False and message.content.lower().startswith(p.lower()):
                ...
            elif message.content.startswith(p):
                ...
            else:
                continue

            return p

        return prefix

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

    async def init_database(self, _) -> None:
        URL = yarl.URL.build(
            scheme="postgres",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=5432,
            path="/" + POSTGRES_DATABASE
        )
        await Tortoise.init(
            db_url=str(URL),
            modules={
                "models": ["builder.database.models"]
            }
        )

        await Tortoise.generate_schemas()

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
        prefix = "b!"

    else:
        record = await Guild.get(guild_id=message.guild_id)
        prefix = record.prefix

    return prefix