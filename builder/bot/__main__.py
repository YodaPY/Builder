import hikari
from builder.config import *
from builder.bot import BuilderBot, get_prefix
from builder.database.client import DBClient

cache_settings = hikari.CacheSettings(
    invites=False,
    voice_states=False,
    messages=False
)

intents = (
    hikari.Intents.GUILD_MEMBERS    |
    hikari.Intents.GUILDS           |
    hikari.Intents.GUILD_MESSAGES
)

bot_settings = {
    "token": TOKEN,
    "prefix": get_prefix,
    "ignore_bots": True,
    "cache_settings": cache_settings,
    "intents": intents
}

database = DBClient(
    database=POSTGRES_DATABASE,
    password=POSTGRES_PASSWORD,
    user=POSTGRES_USER,
    host=POSTGRES_HOST
)

bot = BuilderBot(database, **bot_settings)
bot.run(
    activity=hikari.Activity(
        name="the trading market",
        type=hikari.ActivityType.COMPETING
    )
)