from type import (
    AdminRequired, Cog, Bot, Embed, EmbedGenSlash,
    AppCommandArgs, SlashContext, TextChannel, TimeStampNow,
    ALLOWED_GUILDS
)

class EmbedGenerator(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @EmbedGenSlash
    @AppCommandArgs(
        channel = "Kênh bạn muốn gửi embed",
        title = "Tiêu đề của embed",
        description = "Mô tả của embed",
        color = "Màu của embed",
        timestamp = "Timestamp của embed",
        thumbnail = "Thumbnail của embed",
        image = "Hình ảnh của embed",
        footer = "Footer của embed"
    )
    @AdminRequired
    async def embed_send(self, interaction: SlashContext,
                         channel: TextChannel,
                         description: str,
                         title: str | None = None,
                         color: int | None = None,
                         timestamp: bool = False,
                         thumbnail: str | None = None,
                         image: str | None = None,
                         footer: str | None = None
                        ) -> None:
        if not interaction.guild:
            return

        if not interaction.guild.id in ALLOWED_GUILDS:
            return
        
        embed = Embed(
            title = title,
            description = description,
            color = color,
            timestamp = TimeStampNow() if timestamp else None
        )
        embed.set_footer(text = footer)
        embed.set_thumbnail(url = thumbnail if thumbnail else None)
        embed.set_image(url = image if image else None)

        await interaction.response.defer(ephemeral = True)
        await interaction.followup.send(content = f"Tạo embed thành công tới kênh: {channel.mention}", ephemeral = True)
       
        await channel.send(embed = embed)

async def setup(bot: Bot) -> None:
    await bot.add_cog(EmbedGenerator(bot = bot))