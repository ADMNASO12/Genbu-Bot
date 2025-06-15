import discord
from discord.ext import commands
from discord import AllowedMentions

class GamePingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate = 1, per = 300, type = commands.BucketType.user)
    async def game(self, ctx: commands.Context[commands.Bot], game_name: str | None = None) -> None:
        game_channel_id = 1381577143993237514

        if ctx.channel.id != game_channel_id:
            await ctx.channel.send(content = (
                f"Bạn chỉ có thể sử dụng lệnh này tại kênh <#{game_channel_id}>"
            ))
            return

        if not game_name:
            await ctx.channel.send(content = (
                    f"Vui lòng đề cập tên game bạn muốn bot ping:\n" + 
                    "Những game được hỗ trợ hiện tại và cách dùng:\n" +
                    "* Tên Game: Đấu trường Chân Lý | Sử dụng: `.game tft`\n" + 
                    "* Tên Game: Liên Quân Mobile | Sử dụng: `.game aov`\n" +
                    "* Tên Game: Liên Minh Huyền Thoại | Sử dụng: `.game lol`\n" +
                    "* Tên Game: Genshin Impact | Sử dụng: `.game gi`\n" +
                    "* Tên Game: Minecraft | Sử dụng: `.game mine`\n"
            ))
            return

        game_role: discord.Role | None = None

        match game_name.lower():
            case "tft":
                game_name = "Đấu Trường Chân Lý"

                if ctx.guild:
                    game_role = ctx.guild.get_role(1381575850356506687)

            case "aov":
                game_name = "Liên Quân"

                if ctx.guild:
                    game_role = ctx.guild.get_role(1381575814402936892)

            case "lol":
                game_name = "Liên Minh Huyền Thoại"

                if ctx.guild:
                    game_role = ctx.guild.get_role(1381575713064226898)

            case "gi" | "genshin":
                game_name = "Genshin Impact"

                if ctx.guild:
                    game_role = ctx.guild.get_role(1383635475956236409)

            case "mine" | "minecraft":
                game_name = "Minecraft"

                if ctx.guild:
                    game_role = ctx.guild.get_role(1383635362844508272)

            case _:
                await ctx.channel.send(content = (
                    f"Game: {game_name} không tồn tại hoặc không được hỗ trợ bởi bot.\n" + 
                    "Những game được hỗ trợ hiện tại và cách dùng:\n" +
                    "* Tên Game: Đấu trường Chân Lý | Sử dụng: `.game tft`\n" + 
                    "* Tên Game: Liên Quân Mobile | Sử dụng: `.game aov`\n" +
                    "* Tên Game: Liên Minh Huyền Thoại | Sử dụng: `.game lol`\n" +
                    "* Tên Game: Genshin Impact | Sử dụng: `.game gi`\n" +
                    "* Tên Game: Minecraft | Sử dụng: `.game mine`\n"
                ), allowed_mentions = AllowedMentions(everyone = False, roles = False, users = False))
                return
            
        if game_role:
            await ctx.channel.send(content = (
                f"* {ctx.author.name} muốn mời mọi người cùng chơi game: **{game_name}**\n" +
                f"* {game_role.mention} cùng tham gia nào!"
            ))

    @game.error
    async def on_game_cooldown_error(self, ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(content = (
                "* Bạn chỉ được phép sử dụng lệnh 5 phút một lần.\n" +
                f"* Thời gian chờ còn lại: {round(error.retry_after, 1)} giây."
            ))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GamePingCommand(bot = bot))