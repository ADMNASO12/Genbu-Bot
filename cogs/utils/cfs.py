import discord
from discord.ext import commands
from discord import app_commands


class Cfs(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        # Warning: Replace with YOUR discord channel ID.
        self.CFS_CHANNEL: int = 1047035958857564170
        self.LOG_CHANNEL: int = 1259474965393178727

        self.IMG_URL: str = "https://media.discordapp.net/attachments/1047035958857564170/1358679100734050394/s.jpg?ex=67f4b804&is=67f36684&hm=a4fe836e76fa5f6497b9ac1fd24c98b433858e8fbe97c4e65f4ad77a49eb6b06&=&format=webp"

    @app_commands.command(name = 'confession', description = 'Gửi confession ẩn danh')
    @app_commands.describe(msg = "Tin nhắn bạn muốn gửi ẩn danh")
    async def cfs(self, interaction: discord.Interaction, msg: str) -> None:
        if not interaction.guild:
            return

        img_url: str = self.IMG_URL
        embed = discord.Embed(
            title = "Lời thú tội/tin nhắn ẩn danh",
            description = f'* {msg}',
            color = 0xffa348
        )
        embed.set_thumbnail(url = interaction.guild.icon.url)
        embed.set_image(url = img_url)

        CHANNEL_ID = interaction.guild.get_channel(self.CFS_CHANNEL)
        LOG_CHANNEL_ID = self.bot.get_channel(self.LOG_CHANNEL)

        await interaction.response.defer(ephemeral = True)

        message = await CHANNEL_ID.send(embed = embed)

        await interaction.followup.send(f"Gửi tin nhắn ẩn danh của bạn thành công tới kênh {CHANNEL_ID}", ephemeral = True)
        log_msg = f"Gửi bởi: {interaction.user.name}\nID:{interaction.user.id}\nNội dung: {msg}"

        await LOG_CHANNEL_ID.send(log_msg)

        await message.add_reaction("👍")
        await message.add_reaction("👎")

        await message.create_thread(name = "Bạn nghĩ sao về nội dung của confession này?", auto_archive_duration = 1440)

async def setup(bot) -> None:
    await bot.add_cog(Cfs(bot))
