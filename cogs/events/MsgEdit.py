import discord
import datetime
import logging
from typing import overload, Optional
from discord.ext import commands

class MsgEdit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(1374294073774440528)
        self.logging = logging.basicConfig(
            level = logging.WARNING,
            format = "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.author.bot:
            return

        before_text  = before.content
        after_text   = after.content

        before_urls  = [att.url for att in before.attachments] if before.attachments else []
        after_urls   = [att.url for att in after.attachments] if after.attachments else []

        time_now     = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        text_changed = before_text != after_text
        images_changed = before_urls != after_urls

        if not text_changed and not images_changed:
            return

        log_msg = f"""
* ID người dùng: {before.author.id}
* Đề cập: {before.author.mention}
* Sửa vào lúc: <t:{time_now}>
    """

        if text_changed and not images_changed:
            log_msg += f"\n* Nội dung cũ: {before_text or '[Không có nội dung]'}\n"
            log_msg += f"\n* Nội dung mới: {after_text or '[Không có nội dung]'}\n"
            log_msg += "\n* Phân loại nội dung: Tin nhắn văn bản\n"

            await self.send_log_msg(msg = log_msg)

            return

        if images_changed and not text_changed:
            if before_urls and not after_urls:
                log_msg += "\n* Nội dung cũ: Tin nhắn hình ảnh\n"
                log_msg += "\n* Nội dung mới: [Không có ảnh]\n"
                log_msg += "\n* Phân loại nội dung: Ảnh bị xóa trong lúc sửa\n"

                await self.send_log_msg(msg = log_msg)

                return
            
            elif not before_urls and after_urls:
                log_msg += "\n* Nội dung cũ: [Không có ảnh]\n"
                log_msg += "\n* Nội dung mới: Tin nhắn hình ảnh\n"
                log_msg += "\n* Phân loại nội dung: Ảnh được thêm trong lúc sửa\n"
                image_url = after_urls[0]

                await self.send_log_msg(msg = log_msg, url = image_url)
                return
            
            else:
                log_msg += "\n* Nội dung: Tin nhắn hình ảnh được chỉnh sửa\n"
                image_url = after_urls[0] if after_urls else None

                if image_url:
                    await self.send_log_msg(msg = log_msg, url = image_url)
                else:
                    await self.send_log_msg(msg = log_msg)

                return

        if text_changed and images_changed:

            if before_urls and not after_urls:
                log_msg += f"\n* Nội dung cũ: {before_text or '[Không có nội dung]'} + ảnh\n"
                log_msg += f"\n* Nội dung mới: {after_text or '[Không có nội dung]'} (ảnh bị xóa)\n"
                log_msg += "\n* Phân loại nội dung: Tin nhắn văn bản và ảnh bị xóa\n"
                await self.send_log_msg(msg = log_msg)
                return

            if not before_urls and after_urls:
                log_msg += f"\n* Nội dung cũ: {before_text or '[Không có nội dung]'}\n"
                log_msg += f"\n* Nội dung mới: {after_text or '[Không có nội dung]'} + ảnh\n"
                log_msg += "\n* Phân loại nội dung: Tin nhắn văn bản và ảnh được thêm\n"
                image_url = after_urls[0]
                await self.send_log_msg(msg = log_msg, url = image_url)
                return

            log_msg += f"\n* Nội dung cũ: {before_text or '[Không có nội dung]'} + ảnh\n"
            log_msg += f"\n* Nội dung mới: {after_text or '[Không có nội dung]'} + ảnh\n"
            log_msg += "\n* Phân loại nội dung: Tin nhắn văn bản và ảnh được chỉnh sửa\n"
            image_url = after_urls[0] if after_urls else None

            if image_url:
                await self.send_log_msg(msg = log_msg, url = image_url)
            else:
                await self.send_log_msg(msg = log_msg)

    @overload
    async def send_log_msg(self, msg: str) -> None: ...
    @overload
    async def send_log_msg(self, msg: str, url: str) -> None: ...
       
    async def send_log_msg(self, msg: str, url: Optional[str | None] = None) -> None:
        embed = discord.Embed(
            title = "Tin nhắn vừa được chỉnh sửa",
            description = msg,
            color = 0x2f3136,
            timestamp = datetime.datetime.now()
        )
        
        if url:
            embed.set_image(url = url)

        if isinstance(self.log_channel, discord.TextChannel):
            await self.log_channel.send(embed = embed)

        else:
            logging.warning(f"{self.log_channel} is not a text channel.")
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MsgEdit(bot = bot))