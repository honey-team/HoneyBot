import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import manage_servers_db as manage_db


# bot = commands.Bot(test_guilds=[
#                    1113102018991620228, 972183553775382530], command_prefix=manage_db.get_command_prefix)
bot = commands.InteractionBot(
    test_guilds=[1113102018991620228, 972183553775382530])


@bot.event
async def on_ready():
    print('The bot is ready!')


@bot.event
async def on_guild_join(guild: disnake.Guild):
    await manage_db.add_server(guild.id)


@bot.event
async def on_guild_leave(guild: disnake.Guild):
    await manage_db.remove_server(guild.id)


bot.load_extension("cogs.public_slash_commands")


load_dotenv('token.env')

bot.run(os.getenv('BOT_TOKEN'))
