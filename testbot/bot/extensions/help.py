import discord
from discord.ext import commands

from testbot.bot import Bot


class Help(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: Bot) -> None:
        self.bot = bot


def setup(bot: Bot) -> None:
    bot.add_cog(Help(bot))
