import discord
import asyncio
import datetime
import logging
import requests
from asyncio import tasks
from discord.ext import commands, tasks
from discord import TextInput, app_commands
from discord.ui import Button, TextInput, Modal, View

# Cog, Bot type defined
Bot = commands.Bot
Cog = commands.Cog

# Command permission type defined
AdminRequired = commands.has_guild_permissions(administrator = True)

# Permission
DisablePerm = discord.Permissions.none()

# Command type defined
PrefixComand = commands.command()
OwnerOnly = commands.is_owner()
Context = commands.Context[commands.Bot]

# Error type defined
MissingPermission = commands.MissingPermissions
CommandError = commands.CommandError

# Discord guild, channel, etc... type defined
Channel = discord.abc.GuildChannel
TextChannel = discord.TextChannel
VoiceChannel = discord.VoiceChannel
Category = discord.CategoryChannel
HasChannelType = discord.ChannelType

# Application command slash name
ALLOWED_GUILDS = [
    1045648454170451988,
    1073730331263373372
]
ConfessionSlash = app_commands.command(name = 'confession', description = 'Gửi confession ẩn danh')
EmbedGenSlash = app_commands.command(name = "embed_send", description = "Gửi embed tới 1 kênh nào đó")

# Application command slash argument
AppCommandArgs = app_commands.describe

# Interaction command defined
SlashContext = discord.Interaction

# Cog event defined
CogEvent = commands.Cog.listener

# Asyncio
Sleep = asyncio.sleep

# Embed
Embed = discord.Embed

# Discord Actions
WebhookCreate = discord.AuditLogAction.webhook_create

# Time
TimeStampNow = datetime.datetime.now
TimeStamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

# Member
Member = discord.Member

# Logging
logging.basicConfig(
    level = logging.WARNING,
    format = "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

Warning = logging.warning
Critical = logging.critical

# View, Button, Modal
View = View
Button = Button
Modal = Modal
Text = TextInput
Paragraph = discord.TextStyle.paragraph
Primary = discord.ButtonStyle.primary

# Task loop
TaskLoop = tasks.loop

# Request
RequestGet = requests.get

# Discord Invite
Invite = discord.Invite

# Fallback constain
FALLBACK_THUMBNAIL = "https://images-ext-1.discordapp.net/external/hjLpsPI27iRAXx-cF_exYtbwFBJtEl2yfgQwUXZ3_rc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1043589382671708243/c45fbe666050ab448ab0cf68c14c2284.png?format=webp&quality=lossless&width=584&height=584"