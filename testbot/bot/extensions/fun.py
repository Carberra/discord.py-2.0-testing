import random

import discord
from discord.ext import commands

from testbot.bot import Bot


class Fun(commands.Cog):
    __slots__ = ()

    @commands.command(name="hello", aliases=["hi", "hey"])
    async def command_hello(self, ctx: commands.Context):
        greeting = random.choice(("Hello", "Hi", "Hey", "Hiya", "Heya"))
        await ctx.send(f"{greeting} {ctx.author.mention}!")

    @commands.command(name="dice", aliases=["roll"])
    async def command_dice(self, ctx: commands.Context, dice: int) -> None:
        number, highest = (int(term) for term in dice.split("d"))

        if number > 25:
            return await ctx.send("I can only roll up to 25 dice at a time.")

        rolls = [random.randint(1, highest) for i in range(number)]
        await ctx.send(" + ".join(str(r) for r in rolls) + f" = {sum(rolls)}")


def setup(bot: Bot) -> None:
    bot.add_cog(Fun())
