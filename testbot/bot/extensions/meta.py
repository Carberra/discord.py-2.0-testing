import discord
from discord.ext import commands

from testbot.bot import Bot


class Meta(commands.Cog):
    __slots__ = ()

    @commands.command(name="ping")
    async def command_ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"Pong! Latency: {ctx.bot.latency * 1000:,.0f} ms")


def setup(bot: Bot) -> None:
    bot.add_cog(Meta())
