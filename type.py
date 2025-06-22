import discord
import asyncio
import datetime
from discord.ext import commands
from discord import app_commands

# Cog, Bot type defined
Bot = commands.Bot
Cog = commands.Cog

# Command permission type defined
AdminRequired = commands.has_guild_permissions(administrator = True)

# Permission
DisablePerm = discord.Permissions.none()

# Command type defined
PrefixComand = commands.command()
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
ConfessionSlash = app_commands.command(name = 'confession', description = 'Gửi confession ẩn danh')

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

# Member
Member = discord.Member