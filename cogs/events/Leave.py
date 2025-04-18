import discord
from discord.ext import commands

class LeaveEvent(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        # Warning: Replace with YOUR Discord guild id.
        self.GENBU_ID: int = 1073730331263373372
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.id != self.GENBU_ID:
            print(f"Leave not allowed guild: {guild.name}")
            await guild.leave()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LeaveEvent(bot = bot))