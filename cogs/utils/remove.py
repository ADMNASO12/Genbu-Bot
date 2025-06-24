import discord
import datetime
from typing import Any
from config_load import ConfigLoad
from pymongo import MongoClient
from discord.ext import commands

class Remove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.uri = ConfigLoad.load_config()
        self.client: MongoClient[Any] = MongoClient(self.uri)
        
        self.database = self.client["CustomWords"]
        self.wordsDB = self.database["CustomWords"]

        self.genbu = 1073730331263373372

    def remove_word(self, word: str) -> bool:
        result = self.wordsDB.find_one({"wordsList.word": word})

        if not result:
            return False
        
        self.wordsDB.update_one(
            {"wordsList.word": word},  
            {"$pull": {"wordsList": {"word": word}}},  
            upsert = False
        )
        return True

    # Replace with your mod/admin role.
    @commands.command()
    @commands.has_any_role(
        1073747375245496410, 
        1073731640918032517,
        1044529340207087616
    )
    async def remove(self, ctx: commands.Context[commands.Bot], word: str | None = None) -> None:
        if not ctx.guild:
            return
        
        if ctx.guild.id != self.genbu:
            return

        botUser = ctx.guild.get_member(1334471950755565579)
        
        if word is None:
            embed = discord.Embed(
                description = (
                    f"{ctx.author.name} ơi, hãy nhập từ khóa tùy chỉnh mà bạn muốn xóa\n" + \
                    "`.remove <từ khóa>`" 
                ),
                timestamp = datetime.datetime.now(),
                color = 0x2f3136
            )

            if botUser:
                if botUser.avatar:
                    embed.set_thumbnail(url = botUser.avatar.url)

            await ctx.channel.send(embed = embed)

            return

        if not self.remove_word(word):
            embed = discord.Embed(
                description = (
                    f"{ctx.author.name} ơi, từ khóa tùy chỉnh {word} không tồn tại, " +
                    "bạn không cần xóa từ khóa tùy chỉnh nữa"
                ),
                timestamp = datetime.datetime.now(),
                color = 0x2f3136
            )

            if botUser and botUser.avatar:
                embed.set_thumbnail(url = botUser.avatar.url)

            await ctx.channel.send(embed = embed)
            
            return

        blueDot = "<:dot:1067002963605852201>"
        rightArrow = "<:ArrowRight:1334500913066278986>"

        embed = discord.Embed(
            color = 0x2f3136,
            timestamp = datetime.datetime.now()
        )
        embed.add_field(
            name = f"{ctx.author.name} ơi, mình đã xử lí lệnh của bạn như sau:",
            value = (
                f"{rightArrow} Xóa từ khóa tùy chỉnh:\n\n" +
                f"{blueDot} {word}"
            )
        )

        if botUser and botUser.avatar:
            embed.set_thumbnail(url = botUser.avatar.url)
        
        await ctx.channel.send(embed = embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Remove(bot))