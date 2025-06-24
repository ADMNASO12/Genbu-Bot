import discord
import datetime
from typing import overload, Optional
from discord.ext import commands

class MsgDel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(1374294073774440528)
        self.genbu = 1073730331263373372
    
    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message) -> None:
        if msg.author.bot:
            return
        
        if not msg.guild: 
            return
        
        if msg.guild.id != self.genbu:
            return
        
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
* Xóa vào lúc: <t:{time_now}>

                """
                await self.send_log_msg(msg = log_msg_text)

            case (False, True):
                log_msg_text: str = f"""
* ID người dùng: {msg.author.id}
* Đề cập: {msg.author.mention}
* Nội dung tin nhắn: Hình ảnh
* Phân loại nội dung: Tin nhắn hình ảnh
* Xóa vào lúc: <t:{time_now}>

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
            title = "Tin nhắn vừa bị xóa",
            description = msg,
            color = 0x2f3136,
            timestamp = datetime.datetime.now()
        )
        
        if url:
            embed.set_image(url = url)

        if isinstance(self.log_channel, discord.TextChannel):
            await self.log_channel.send(embed = embed)        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MsgDel(bot = bot))