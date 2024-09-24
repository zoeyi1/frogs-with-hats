import discord
import os
from discord import app_commands
from discord.ext import commands
from keepAlive import keepAlive

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
intent.presences = True
bot = commands.Bot(intents = intent, command_prefix = "bbb ")

synced = False  # track if commands have already been synced

@bot.event
async def on_ready():
  global synced
  await bot.change_presence(activity=discord.Game("frogs with hats."))

  if not synced:  # ensure syncing happens only once
    await bot.tree.sync()
    synced = True
    print(f"Bot synced and ready as {bot.user}")

"""
# example ephemeral
@bot.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"hi {interaction.user.mention}", ephemeral = True)

# example slash command
@bot.tree.command(name = "say", description = "this is a description")
@app_commands.describe(thing_to_say = "what should i say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
  await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")
"""

@bot.tree.command(name="dm", description = "dont go ham")
@app_commands.describe(user="The user to send a DM to", message="The message to send")
async def dm(interaction: discord.Interaction, user: discord.Member, message: str):
    try:
        # Send a DM to the specified user with a mention (ping)
        await user.send(f"<@{user.id}> {message}")  # This will ping the user
        # Send confirmation in the interaction channel
        await interaction.response.send_message(f"Sent a DM to {user.mention}!", ephemeral=True)
    except discord.Forbidden:
        # In case the bot cannot send a DM (e.g., user has DMs disabled)
        await interaction.response.send_message(f"Unable to send a DM to {user.mention}. They might have DMs disabled.", ephemeral=True)

keepAlive()
my_secret = os.environ['TOKEN']
bot.run(my_secret)