from discord.ext import commands

from testbot.bot import Bot


class ErrorHandler:
    __slots__ = ()

    async def command_error(self, ctx: commands.Context, exc: Exception):
        if isinstance(exc, commands.CommandNotFound):
            return

        if isinstance(exc, commands.MissingRequiredArgument):
            return await ctx.send("One or more required arguments are missing.")

        if isinstance(exc, commands.BadArgument):
            return await ctx.send(f"One or more arguments are invalid")

        if isinstance(exc, commands.MissingPermissions):
            return await ctx.send("You are missing some required permissions.")

        if isinstance(exc, commands.BotMissingPermissions):
            return await ctx.send("I am missing some required permissions.")

        if isinstance(exc, commands.NotOwner):
            return await ctx.send("You are not my owner.")

        raise exc


def setup(bot: Bot) -> None:
    bot.error_handler = ErrorHandler()
