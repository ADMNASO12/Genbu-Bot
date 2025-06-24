import discord
import datetime
import logging
from typing import overload, Optional, Any
from config_load import ConfigLoad
from pymongo.mongo_client import MongoClient
from discord.ext import commands

class CustomWords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(1386929447827017909)
        self.logging = logging.basicConfig(
            level = logging.WARNING,
            format = "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )

        self.mongo_env = ConfigLoad.load_config()
        self.client: MongoClient[Any] = MongoClient(self.mongo_env)

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
        genbu = 1073730331263373372

        if message.author.bot:
                return
            
        if not message.guild or message.guild.id != genbu:
                return

        msg = self.find_words(message.content)
        if msg:
            await message.channel.send(msg, allowed_mentions = discord.AllowedMentions.none())
            
        else:
                msg = message
                msg_text: str = msg.content
                attachments = msg.attachments
                time_now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

                match (bool(msg_text), bool(attachments)):
                    case (True, False):
                        log_msg_text: str = f"""
* ID người dùng: {msg.author.id}
* Đề cập: {msg.author.mention}
* Nội dung tin nhắn: {msg_text}
* Phân loại nội dung: Tin nhắn văn bản
* Gửi vào lúc: <t:{time_now}>

                        """
                        await self.send_log_msg(msg = log_msg_text)

                    case (False, True):
                        log_msg_text: str = f"""
* ID người dùng: {msg.author.id}
* Đề cập: {msg.author.mention}
* Nội dung tin nhắn: Hình ảnh
* Phân loại nội dung: Tin nhắn hình ảnh
* Gửi vào lúc: <t:{time_now}>

                        """
                        image_url = attachments[0].url
                        await self.send_log_msg(msg = log_msg_text, url = image_url)
                    
                    case _:
                        pass
        
    @overload
    async def send_log_msg(self, msg: str) -> None: ...
    @overload
    async def send_log_msg(self, msg: str, url: str) -> None: ...
       
    async def send_log_msg(self, msg: str, url: Optional[str] = None) -> None:
        embed = discord.Embed(
            title = "Tin nhắn vừa được gửi đi",
            description = msg,
            color = 0x2f3136,
            timestamp = datetime.datetime.now()
        )
        
        if url:
            embed.set_image(url = url)

        if isinstance(self.log_channel, discord.TextChannel):
            await self.log_channel.send(embed = embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CustomWords(bot))