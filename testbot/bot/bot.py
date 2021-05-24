import traceback
from pathlib import Path

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands, fancyhelp
from pytz import utc

from testbot import __version__

MAIN_GUILD_ID = 845688627265536010
STDOUT_CHANNEL_ID = 845691044527210515


class Bot(commands.Bot):
    __slots__ = ("ready", "extensions", "scheduler", "error_handler")

    def __init__(self) -> None:
        self.ready = False
        self.extensions = [p.stem for p in Path(".").glob("./testbot/bot/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        self.error_handler = None

        super().__init__(
            command_prefix="-",
            case_insensitive=True,
            intents=discord.Intents.all(),
            help_command=fancyhelp.EmbeddedHelpCommand(),
            activity=discord.Activity(
                name=f"-help | Version {__version__}",
                type=discord.ActivityType.watching,
            ),
        )

    def setup(self) -> None:
        print("Running setup...")
        for ext in self.extensions:
            self.load_extension(f"testbot.bot.extensions.{ext}")
            print(f" `{ext}` extension loaded.")

    def run(self) -> None:
        self.setup()

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read()

        print("Running bot...")
        super().run(token, reconnect=True)

    async def close(self) -> None:
        print("Shutting down...")
        self.scheduler.shutdown()
        await self.stdout.send(f"Shutting down testbot v{__version__}.")
        await super().close()

    async def on_connect(self) -> None:
        print(f" Bot connected. DWSP latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print(f" Bot disconnected.")

    async def on_error(self, err: str, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        traceback.print_exc()

    async def on_command_error(self, ctx: commands.Context, exc: Exception):
        await self.error_handler.command_error(ctx, exc)

    async def on_ready(self) -> None:
        if self.ready:
            return

        self.guild = self.get_guild(MAIN_GUILD_ID)
        self.stdout = self.guild.get_channel(STDOUT_CHANNEL_ID)

        self.scheduler.start()
        print(f" Scheduler started ({len(self.scheduler.get_jobs()):,} job(s) scheduled)")

        await self.stdout.send(f"testbot v{__version__} is online!")
        self.ready = True
        print(" Bot ready!")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        await self.process_commands(message)

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)
