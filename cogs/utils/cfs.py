import discord
from discord.abc import Messageable
from type import (
    Bot, Embed, HasChannelType, AppCommandArgs, ConfessionSlash,
    Cog, Primary, SlashContext, TextChannel, View, Button, Modal, Text, Paragraph
)

class ReplyField(Modal):
    def __init__(self, origin_msg: discord.Message, bot: Bot) -> None:
        super().__init__(title = "Nhập nội dung")
        self.origin_msg = origin_msg
        self.bot = bot

        self.reply: Text = Text(  # type: ignore
            label = "Nội dung bạn muốn phản hồi", style = Paragraph,
            placeholder = "Vui lòng nhập nội dung", 
            required = True
        ) 
        self.reply.callback = self.on_submit # type: ignore
        self.add_item(self.reply) # type: ignore
        self.IMG_URL: str = "https://media.discordapp.net/attachments/1047035958857564170/1358679100734050394/s.jpg?ex=67f4b804&is=67f36684&hm=a4fe836e76fa5f6497b9ac1fd24c98b433858e8fbe97c4e65f4ad77a49eb6b06&=&format=webp"
        self.LOG_CHANNEL = 1259474965393178727
    
    async def on_submit(self, interaction: SlashContext) -> None:
        if not interaction.guild:
            return
        
        embed = Embed(
            title = "Trả lời tin nhắn ẩn danh",
            description = (
                f"* {self.reply.value}" # type: ignore
            ),
            color = 0xffa348
        )

        if interaction.guild.icon:
            embed.set_thumbnail(url = interaction.guild.icon.url)

        embed.set_image(url = self.IMG_URL)

        await interaction.response.defer()
        message = await self.origin_msg.reply(embed = embed, view = ReplyButton(self.bot)) 

        await message.add_reaction("👍")
        await message.add_reaction("👎")

        await message.create_thread(name = "Bạn nghĩ sao về nội dung của confession này?", auto_archive_duration = 1440)

        LOG_CHANNEL = self.bot.get_channel(self.LOG_CHANNEL)
        if LOG_CHANNEL and isinstance(LOG_CHANNEL, TextChannel):
            await LOG_CHANNEL.send(
                content = (
                    "* Tin nhắn ẩn danh\n" +
                    f"* Nội dung: {self.reply.value}\n" + # type: ignore
                    f"* Người gửi: {interaction.user.name}\n" +
                    f"* ID: {interaction.user.id}"
                )
            )


class ReplyButton(View):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

        reply_button = Button(  # type: ignore
            label = "Trả lời tin nhắn ẩn danh",
            style = Primary
        )
        reply_button.callback = self.on_reply_click
        self.add_item(reply_button) # type: ignore
        
    async def on_reply_click(self, interaction: SlashContext) -> None:
        if interaction.message:
            await interaction.response.send_modal(ReplyField(interaction.message, self.bot))

class Cfs(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        # Warning: Replace with YOUR discord channel ID.

        # Production
        #self.CFS_CHANNEL: int = 1259484204572479562
        self.CFS_CHANNEL: int = 1047035958857564170
        self.LOG_CHANNEL: int = 1259474965393178727

        self.IMG_URL: str = "https://media.discordapp.net/attachments/1047035958857564170/1358679100734050394/s.jpg?ex=67f4b804&is=67f36684&hm=a4fe836e76fa5f6497b9ac1fd24c98b433858e8fbe97c4e65f4ad77a49eb6b06&=&format=webp"

    @ConfessionSlash
    @AppCommandArgs(
        msg = "Tin nhắn bạn muốn gửi ẩn danh",
        img = "Hình ảnh (Nếu có)"
    )
    async def cfs(self, interaction: SlashContext, msg: str, img: str | None) -> None:
        if interaction.guild:

            img_url: str = self.IMG_URL
            embed = discord.Embed(
                title = "Lời thú tội/tin nhắn ẩn danh",
                description = f'* {msg}',
                color = 0xffa348
            )
            if interaction.guild.icon:
                embed.set_thumbnail(url = interaction.guild.icon.url)

            if not img:
                embed.set_image(url = img_url)
            
            else:
                embed.set_image(url = img)

            CHANNEL_ID = interaction.guild.get_channel(self.CFS_CHANNEL)
            LOG_CHANNEL_ID = self.bot.get_channel(self.LOG_CHANNEL)

            await interaction.response.defer(ephemeral = True)

            if CHANNEL_ID and CHANNEL_ID.type == HasChannelType.text:
                message = await CHANNEL_ID.send(embed = embed, view = ReplyButton(self.bot))

                await interaction.followup.send(f"Gửi tin nhắn ẩn danh của bạn thành công tới kênh {CHANNEL_ID}", ephemeral = True)
                log_msg = f"Gửi bởi: {interaction.user.name}\nID:{interaction.user.id}\nNội dung: {msg}"
                
                if isinstance(LOG_CHANNEL_ID, Messageable):
                    await LOG_CHANNEL_ID.send(log_msg)

                await message.add_reaction("👍")
                await message.add_reaction("👎")

                await message.create_thread(name = "Bạn nghĩ sao về nội dung của confession này?", auto_archive_duration = 1440)

        else:
            genbu = self.bot.get_guild(1073730331263373372)

            if genbu:
                img_url: str = self.IMG_URL
                embed = discord.Embed(
                    title = "Lời thú tội/tin nhắn ẩn danh",
                    description = f'* {msg}',
                    color = 0xffa348
                )
                if genbu.icon:
                    embed.set_thumbnail(url = genbu.icon.url)

                if not img:
                    embed.set_image(url = img_url)
                    
                else:
                    embed.set_image(url = img)

                CHANNEL_ID = genbu.get_channel(self.CFS_CHANNEL) # type: ignore
                LOG_CHANNEL_ID = self.bot.get_channel(self.LOG_CHANNEL) # type: ignore
                FAKE_LOG_CHANNEL_ID = self.bot.get_channel(1386222643979620443) # type: ignore

                await interaction.response.defer(ephemeral = True)

                if CHANNEL_ID and CHANNEL_ID.type == HasChannelType.text:
                    message = await CHANNEL_ID.send(embed = embed)

                    await interaction.followup.send(f"Gửi tin nhắn ẩn danh của bạn thành công tới kênh {CHANNEL_ID}", ephemeral = True)
                    log_msg = f"Gửi bởi: {interaction.user.name}\nID:{interaction.user.id}\nNội dung: {msg}"
                    
                    if isinstance(LOG_CHANNEL_ID, Messageable):
                        await LOG_CHANNEL_ID.send(log_msg)

                    await message.add_reaction("👍")
                    await message.add_reaction("👎")

                    await message.create_thread(name = "Bạn nghĩ sao về nội dung của confession này?", auto_archive_duration = 1440)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Cfs(bot))