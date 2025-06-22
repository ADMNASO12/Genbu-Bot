import discord
from discord.ext import commands
from discord import app_commands

# Cog, Bot type defined
Bot = commands.Bot
Cog = commands.Cog

# Command permission type defined
AdminRequired = commands.has_guild_permissions(administrator = True)

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