import discord
import datetime
from config_load import ConfigLoad
from pymongo.mongo_client import MongoClient
from discord.ext import commands

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.uri = ConfigLoad.load_config()
        self.client = MongoClient(self.uri)
        self.database = self.client["CustomWords"]
        self.wordsDB = self.database["CustomWords"]

    def add_word(self, word: str, msg: str) -> bool:       
        result = self.wordsDB.find_one({"wordsList.word": word})
        
        if result:
            return False
    
        self.wordsDB.update_one(
            {},  
            {"$push": {"wordsList": {"word": word, "msg": msg}}},  
            upsert = True  
        )
        return True
    
    @commands.command()
    @commands.has_any_role(
        1073747375245496410, 
        1073731640918032517,
        1044529340207087616
    )
    async def add(self, ctx: commands.Context, words: str = None, *, msg: str = None) -> None:
        if not ctx.guild:
            return

        botUser = ctx.guild.get_member(1334471950755565579)
        
        if words is None:
            embed = discord.Embed(
                description = (
                    f"{ctx.author.name} ơi, hãy nhập từ khóa tùy chỉnh mà bạn muốn thêm nhé\n" + \
                    "`.add <từ khóa> <Nội dung>`\n\n" +
                    f"TIPS: Nếu như {ctx.author.name} muốn thêm từ khóa có chứa dấu cách, sử dụng lệnh như sau;\n\n" + \
                    ".add  \"<từ khóa>\" <nội dung>"
                ),
                color = 0x2f3136,
                timestamp = datetime.datetime.now()
            )
            embed.set_thumbnail(url = botUser.avatar.url)
            
            await ctx.channel.send(embed = embed)
            return

        if msg is None:
            embed = discord.Embed(
                description = (
                    f"{ctx.author.name} ơi, hãy nhập nội dung tùy chỉnh mà bạn muốn thêm nhé\n" + \
                    "`.add <từ khóa> <Nội dung>`\n\n" + \
                    f"TIPS: Nếu như {ctx.author.name} muốn thêm nội dung tùy chỉnh có chứa dấu cách, sử dụng lệnh như sau;\n\n" + \
                    ".add  \"<từ khóa>\" <nội dung>"
                ),
                color = 0x2f3136,
                timestamp = datetime.datetime.now()
            )
            embed.set_thumbnail(url = botUser.avatar.url)
            
            await ctx.channel.send(embed = embed)
            return

        blueDot = "<:dot:1067002963605852201>"
        rightArrow = "<:ArrowRight:1334500913066278986>"

        if self.add_word(words, msg):
            embed = discord.Embed(
                timestamp = datetime.datetime.now(),
                color = 0x2f3136
            )
            embed.add_field(
                name = f"{ctx.author.name} ơi, mình đã xử lí lệnh của bạn như sau",
                value = (
                    f"{blueDot} Từ khóa: {words}\n\n" + \
                    f"{rightArrow} Nội dung: {msg}"
                )
            )
            embed.set_thumbnail(url = botUser.avatar.url)

            await ctx.channel.send(embed = embed)
            return

        await ctx.channel.send(f"{ctx.author.name} ơi, từ khóa tùy chỉnh {words} đã tồn tại rồi!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Add(bot))