import discord
import json
from discord.ext import commands

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
    "cogs.utils.cfs"
]

async def setupCogs() -> None:
    for cog in cogList:
        await bot.load_extension(cog)
        print(f"Loaded {cog} successfully")

@bot.event
async def on_ready() -> None:
    await setupCogs()
    await bot.tree.sync()
    print(f"Online as {bot.user}")

if(__name__ == "__main__"):
    bot.run(BOT_TOKEN)