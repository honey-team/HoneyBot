import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import manage_servers_db as manage_db
from datetime import datetime


# bot = commands.Bot(test_guilds=[
#                    1113102018991620228, 972183553775382530], command_prefix=manage_db.get_command_prefix)
bot = commands.InteractionBot(
    test_guilds=[1113102018991620228, 972183553775382530])


bot.load_extension("cogs.events")
bot.load_extension("cogs.public_slash_commands")


load_dotenv('token.env')

bot.run(os.getenv('BOT_TOKEN'))
