import discord
from discord.ext import commands

from testbot.bot import Bot

JAX_ID = 135372594953060352
QT_EMOTE_ID = "<:qt:845700343195238431>"


class Qt(commands.Cog):
    __slots__ = ()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.id != JAX_ID:
            return

        await message.add_reaction(QT_EMOTE_ID)


def setup(bot: Bot) -> None:
    bot.add_cog(Qt())
