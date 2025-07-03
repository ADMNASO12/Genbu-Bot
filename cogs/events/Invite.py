from type import (
    Cog, Bot, CogEvent, Embed, Invite, TextChannel, TimeStamp,
    Warning
)

class InviteManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.LOG_CHANNEL = self.bot.get_channel(1091479187430322266)

    @CogEvent()
    async def on_invite_create(self, invite: Invite) -> None:
        print("event trigger....")
        if invite.guild:
            embed = Embed(
                title = "Hệ thống phòng thủ Romans | Cảnh báo",
                description = (
                    "* Vừa có một invite được tạo:\n\n" +
                    f"* Người tạo: {invite.inviter}\n" +
                    f"* Tạo vào lúc: <t:{TimeStamp}>\n" + 
                    f"* Mã mời: `{invite.code}`\n" + 
                    f"* Hết hạn vào lúc: `{invite.expires_at}`"
                ),
                color = 0xecca86
            )

            if self.LOG_CHANNEL and isinstance(self.LOG_CHANNEL, TextChannel):
                await self.LOG_CHANNEL.send(embed = embed)

            else:
                Warning(f"[Module Invite Manager] {self.LOG_CHANNEL} is not a TextChannel")
        
async def setup(bot: Bot) -> None:
    await bot.add_cog(InviteManager(bot = bot))