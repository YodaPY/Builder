import hikari
from enum import Enum
from typing import Union
from lightbulb import Context as _Context
from builder.bot import Guild

__all__ = ("TranslationType", "Context")

class TranslationType(Enum):
    Text = 1
    Embed = 2
    Docs = 3

class Context(_Context):
    __slots__ = ()

    async def language(self) -> str:
        """
        Get the language set for a server
        """

        record = await Guild.get(guild_id=self.guild_id)

        return record.lang

    async def translate_message(self, t_type: TranslationType, index: int, /) -> Union[str, hikari.Embed]:
        """
        Get the translated message for a server

        Params:
            t_type (TranslationType): The type of translation (Text, Embed)
            index (int): The translated message that should be used
        """

        command = self.command.qualified_name.replace(" ", ".")
        lang = await self.language()

        translation = self.bot.translations[lang][command][t_type.name][index]

        if isinstance(translation, dict):
            return self.bot.entity_factory.deserialize_embed(translation)

        return translation