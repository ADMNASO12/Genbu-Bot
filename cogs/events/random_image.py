from type import (
    Cog, Bot, Embed, TaskLoop, TextChannel,
    RequestGet, Warning, View, Button
)

class DownloadButton(View):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
        self.add_item(Button(
             label = "Tải hình ảnh xuống",
             url = self.url
        ))

class RandomImage(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.api_endpoint = "https://nekos.best/api/v2/waifu"
        self.fallback_thumbnail = "https://images-ext-1.discordapp.net/external/hjLpsPI27iRAXx-cF_exYtbwFBJtEl2yfgQwUXZ3_rc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1043589382671708243/c45fbe666050ab448ab0cf68c14c2284.png?format=webp&quality=lossless&width=584&height=584"
        self.random_image.start()

    @TaskLoop(seconds = 300)
    async def random_image(self):
        channel = self.bot.get_channel(1257053670269517934)
        genbu = self.bot.get_guild(1073730331263373372)

        if genbu:
            if channel and isinstance(channel, TextChannel):

                    response = RequestGet(url = self.api_endpoint)
                    json_data = response.json()
                    image_url = json_data["results"][0]["url"]

                    embed = Embed(
                        title = "Một hình ảnh ngẫu nhiên mỗi 5 phút",
                        color = 0x83ff88
                    )
                    embed.set_thumbnail(url = genbu.icon.url if genbu.icon else self.fallback_thumbnail)
                    embed.set_image(url = image_url)

                    message = await channel.send(embed = embed, view = DownloadButton(image_url))
                    await message.add_reaction("👍")
                    await message.add_reaction("👎")

            else:
                Warning(f"In module: RandomImage {channel} is not a text channel or unknown")

        else:
             Warning(f"In module: RandomImage {genbu} is None or unknown guild")         

async def setup(bot: Bot) -> None:
    await bot.add_cog(RandomImage(bot = bot))