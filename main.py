import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands


# bot = commands.Bot(test_guilds=[
#                    1113102018991620228, 972183553775382530], command_prefix=manage_db.get_command_prefix)

intents = disnake.Intents.default()
intents.members = True

bot = commands.InteractionBot(
    test_guilds=[1113102018991620228, 972183553775382530], intents=intents)


bot.load_extension("cogs.events")
bot.load_extension("cogs.public_slash_commands")


load_dotenv('token.env')

bot.run(os.getenv('BOT_TOKEN'))
