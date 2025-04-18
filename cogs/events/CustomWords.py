import discord
from config_load import ConfigLoad
from pymongo.mongo_client import MongoClient
from discord.ext import commands

class CustomWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.mongo_env = ConfigLoad.load_config()
        self.client = MongoClient(self.mongo_env)

        self.database = self.client["CustomWords"]
        self.wordsDB = self.database["CustomWords"]

    def find_words(self, words: str):
        result = self.wordsDB.find_one(
            {"wordsList.word": words},
            {"wordsList.$": 1}
        )

        return result["wordsList"][0]["msg"] if result else None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if message.author.bot:
            return
        
        if not message.guild:
            return

        msg = self.find_words(message.content)
        if msg:
            await message.channel.send(msg, allowed_mentions = discord.AllowedMentions.none())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CustomWords(bot))