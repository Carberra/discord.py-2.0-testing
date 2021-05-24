from discord.ext import commands

from testbot import __version__
from testbot.bot import Bot


class Admin(commands.Cog):
    __slots__ = ()

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def command_shutdown(self, ctx: commands.Context) -> None:
        await ctx.bot.close()


def setup(bot: Bot) -> None:
    bot.add_cog(Admin())
