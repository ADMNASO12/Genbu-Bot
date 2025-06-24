import discord
import json
from discord.ext import commands


# Same main.py, but we test here.
with open("./config/config_test.json") as configFile:
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
    "cogs.utils.game_ping",
    "cogs.anti_raid.webhook"
]

async def setupCogs() -> None:
    for cog in cogList:
        await bot.load_extension(cog)
        print(f"Loaded {cog} successfully")

@bot.event
async def on_ready() -> None:
    await setupCogs()
    # for  guild  in ALLOWED_GUILDS:
    await bot.tree.sync(guild = discord.Object(id = 1045648454170451988))

    print(f"Online as {bot.user}")


bot.run(BOT_TOKEN)