from type import (
    Cog, Bot, CogEvent, Channel, DisablePerm, Sleep, TextChannel,
    WebhookCreate, Embed, Member, TimeStampNow
)

class WebhookManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.LOG_CHANNEL = self.bot.get_channel(1386462290806571019)
        self.white_list = [
            1043482116127727666,
            559426966151757824
        ]
        self.allowed_server = [
            1073730331263373372
        ]


    async def __send_alert(self, channel: TextChannel, member: Member) -> None:
        embed = Embed(
            title = "Hệ thống phòng thủ Romans",
            description = (
                "* Loại hành động được phát hiện: **Tạo Webhook**\n\n" +
                "* Hành động phòng thủ: **Xóa Webhook**\n\n" + 
                f"* Đối tượng thực hiện hành động: {member.name}\n\n" + 
                f"* ID đối tượng: {member.id}"
            ),
            color = 0xddb750,
            timestamp = TimeStampNow()
        )
        if member.avatar:
            embed.set_thumbnail(url = member.avatar.url)
    
        await channel.send(embed = embed)

    @CogEvent()
    async def on_webhooks_update(self, channel: Channel) -> None:
        await Sleep(1)

        guild = channel.guild

        if guild and guild.id in self.allowed_server:
            async for entry in guild.audit_logs(limit = 10, action = WebhookCreate):
                if entry.action == WebhookCreate:

                    if entry.user and entry.user.id in self.white_list:
                        print(f"Ignore white list")
                        return

                    webhook_id = entry.target.id if entry.target else None
                    if not isinstance(channel, TextChannel):
                        return
                    
                    webhooks = await channel.webhooks()
                    webhook_object = next((
                        webhook for webhook in webhooks if webhook.id == webhook_id
                    ), None)
                
                    if webhook_object:
                        try:
                            await webhook_object.delete(reason = "Anti-raid webhook create")
                        except Exception as error:
                            print(f"Fatal error when create webhook, in webhook module: {error}")
                        
                        if entry.user:

                            member = guild.get_member(entry.user.id)
                            if member:
                                try:
                                    await member.edit(roles = [], reason = "Anti-raid punished")
                                except Exception as error:
                                    print(f"Fatal error in webhook module, when clear role {error}")

                                if member.bot:

                                    bot_role = guild.get_role(member.id)
                                    if bot_role:
                                        try:
                                            await member.edit(roles = [], reason = "Anti-raid punished")
                                            await bot_role.edit(permissions = DisablePerm)

                                        except Exception as error:
                                            print(f"Fatal error in webhook module, when clear role {error}")


                            if self.LOG_CHANNEL and isinstance(self.LOG_CHANNEL, TextChannel):
                                
                                member = guild.get_member(entry.user.id)
                                if member:
                                    await self.__send_alert(self.LOG_CHANNEL, member = member)
        
                    break

async def setup(bot: Bot) -> None:
    await bot.add_cog(WebhookManager(bot = bot))