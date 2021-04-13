import hikari
from lightbulb import when_mentioned_or
from builder.config import TOKEN
from builder.bot import BuilderBot, get_prefix

cache_settings = hikari.CacheSettings(
    invites=False,
    voice_states=False,
    messages=False
)

intents = (
    hikari.Intents.GUILD_MEMBERS    |
    hikari.Intents.GUILDS           |
    hikari.Intents.GUILD_MESSAGES   |
    hikari.Intents.ALL_MESSAGE_REACTIONS
)

bot_settings = {
    "token": TOKEN,
    "prefix": when_mentioned_or(get_prefix),
    "ignore_bots": True,
    "cache_settings": cache_settings,
    "intents": intents
}

bot = BuilderBot(**bot_settings)
bot.run(
    activity=hikari.Activity(
        name="the trading market",
        type=hikari.ActivityType.COMPETING
    )
)