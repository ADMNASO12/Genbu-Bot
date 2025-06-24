import discord
import json
from discord.ext import commands
from typing import Literal, Optional

from type import Context

with open("./config/config.json") as configFile:
    data = json.load(configFile)
    BOT_TOKEN = data["BOT_TOKEN"]
    BOT_PREFIX = data["BOT_PREFIX"]

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(
    intents = intents,
    command_prefix = BOT_PREFIX
)

cogList = [
    "cogs.owner.RoleInfo",
    "cogs.events.CustomWords",
    "cogs.events.Leave",
    "cogs.utils.add",
    "cogs.utils.remove",
    "cogs.utils.cfs",
    "cogs.utils.embed",
    "cogs.events.MsgDel",
    "cogs.events.MsgEdit",
    "cogs.utils.game_ping"
]

async def setupCogs() -> None:
    for cog in cogList:
        await bot.load_extension(cog)
        print(f"Loaded {cog} successfully")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild = ctx.guild)
        elif spec == "*":
            if ctx.guild:
                ctx.bot.tree.copy_global_to(guild = ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild = None)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.event
async def on_ready() -> None:
    await setupCogs()
    #bot.tree.clear_commands(guild = None)
    await bot.tree.sync()

    for cmd in bot.tree.walk_commands():
        print(f"Load slash: {cmd.name}")

    print(f"Online as {bot.user}")

if(__name__ == "__main__"):
    bot.run(BOT_TOKEN)
