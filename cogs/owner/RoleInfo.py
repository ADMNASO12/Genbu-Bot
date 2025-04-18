import discord
from discord.ext import commands

class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleinfo(self, ctx: commands.Context) -> None:
        if ctx.author.id != 1043482116127727666:
            return
        
        if not ctx.guild:
            return

        # ADMIN, MODERATOR ROLES LIST
        modRole = ctx.guild.get_role(1073747375245496410)
        superModRole = ctx.guild.get_role(1073747635086839889)
        adminRole = ctx.guild.get_role(1073731640918032517)

        # LEVELED ROLES LIST
        anemoRole = ctx.guild.get_role(1073821213081739304)
        geoRole = ctx.guild.get_role(1073821489100509186)
        electroRole = ctx.guild.get_role(1073821705321066596)
        dendroRole = ctx.guild.get_role(1073822030257979522)
        hydroRole = ctx.guild.get_role(1073822753385349130)
        pyroRole = ctx.guild.get_role(1073823532217278506)
        cryoRole = ctx.guild.get_role(1073824032262213712)

        #BOOSTER ROLE
        boosterRole = ctx.guild.get_role(1074230869134413854)

        blueDot = "<:dot:1067002963605852201>"
        rightArrow = "<:ArrowRight:1334500913066278986>"
        expIco = "<:exp:1334502147684827208>"

        embed = discord.Embed(
            title = f'Thông tin về các vai trò trong {ctx.guild.name}',
            color = 0x2f3136
        )
        embed.add_field(
            name = "Các vai trò Admin/Moderator",
            value = (
                f"{rightArrow} Đây là những vai trò quản lí server. Những người có vai trò này "
                "là những người đầu tiên mà bạn nên liên hệ khi bạn gặp những vấn đề "
                "nào đó trong server\n\n"
                f"{blueDot} {adminRole.mention} **Admin của server**\n\n"
                f"{blueDot} {superModRole.mention} **SuperMod của server**\n\n"
                f"{blueDot} {modRole.mention} **Mod của server**\n\n"
            ),
            inline = False
        )
        embed.add_field(
            name = "Các vai trò cấp độ",
            value = (
                f"{rightArrow} Đây là những vai trò mà bạn sẽ nhận được khi " +
                "tương tác tại máy chủ. Mỗi khi bạn chat tại đây. bạn sẽ nhận được " +
                f"một lượng {expIco}, khi đạt đủ các mốc {expIco}, " +
                "nhất định, bạn sẽ nhận được những **Vision** tương ứng:\n\n" +
                f"{blueDot} {anemoRole.mention} **5000** {expIco}\n\n" +
                f"{blueDot} {geoRole.mention} **30.000** {expIco}\n\n" +
                f"{blueDot} {electroRole.mention} **65.000** {expIco}\n\n" +
                f"{blueDot} {dendroRole.mention} **144.000** {expIco}\n\n" +
                f"{blueDot} {hydroRole.mention} **256.000** {expIco}\n\n" +
                f"{blueDot} {pyroRole.mention} **475.000** {expIco}\n\n" +
                f"{blueDot} {cryoRole.mention} **862.000** {expIco}"
            ),
            inline = False
        )
        embed.add_field(
            name = "Những vai trò custom",
            value = (
                f"{rightArrow} Đây là những vai trò đặc biệt dành cho những cá nhân " +
                "hoặc những nhóm người, hay trong những sự kiện đặc biệt. " +
                "Bạn có thể nhận những vai trò custom nếu đã sở hữu vai trò:\n\n" +
                f"{blueDot} {boosterRole.mention}\n\nBạn sẽ được duy  trì vai trò này cho tới khi " +
                "ngừng boost server.\n\n" +
                f"{rightArrow} Ngoài ra bạn cũng hoàn toàn có thể sở hữu những vai trò " +
                "custom độc nhất nếu như gây ấn tượng cho các Admin/Moderator của server, " +
                "tuy nhiên cách đơn giản nhất vẫn là **tương tác tại máy chủ**"
            ),
            inline = False
        )
        embed.set_thumbnail(url = ctx.guild.icon.url)

        await ctx.channel.send(embed = embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RoleInfo(bot))