from type import (
    Cog, Bot, CogEvent, Critical, Member, TextChannel, TimeStampNow,
    Warning, Embed, TimeStamp
)

class WelcomeManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.genbu = 1073730331263373372
        self.welcome_channel = self.bot.get_channel(1073740371923837048)
        self.general_chat = self.bot.get_channel(1073730331766698095)
        self.gif_welcome = "https://www.icegif.com/wp-content/uploads/2022/05/icegif-954.gif"

    @CogEvent()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id != self.genbu:
            return
        
        if not self.welcome_channel:
            Warning(f"[In Welcome Module]: Could not find channel: {self.welcome_channel}")
            return
        
        if not self.general_chat:
            Warning(f"[In Welcome Module]: Could not find channel: {self.general_chat}")
        
        if not isinstance(self.welcome_channel, TextChannel):
            Critical(f"[In Welcome Module]: {self.welcome_channel} is not a text channel")
            return
        
        if not isinstance(self.general_chat, TextChannel):
            Critical(f"[In Welcome Module]: {self.general_chat} is not a text channel")
            return
        
        embed = Embed(
            title = "Chào mừng bạn đã tham gia Genbu Impact",
            description = (
                f"* {member.name} vừa tham gia {member.guild.name}\n\n" +
                f"* Tham gia vào lúc: <t:{TimeStamp}>\n\n" + 
                f"* Đọc quy tắc máy chủ tại đây: {(
                    member.guild.rules_channel.mention
                    if member.guild.rules_channel
                    else 'Unknown Channel'
                )}\n\n" +
                f"* Chọn cho mình những vai trò đẹp tại: <id:customize>"
            ),
            color = 0xd594e6,
            timestamp = TimeStampNow()
        )
        embed.set_footer(text = f"Bạn hiện là thành viên thứ: {member.guild.member_count} của {member.guild.name}")
        
        if member.avatar:
            embed.set_thumbnail(url = f"{member.avatar.url}")
        embed.set_image(url = self.gif_welcome)

        await self.welcome_channel.send(embed = embed)
        await self.general_chat.send(content = f"* {member.mention} vừa tham gia **{member.guild.name}**, cùng chào đón họ nào!")
        
async def setup(bot: Bot) -> None:
    await bot.add_cog(WelcomeManager(bot = bot))