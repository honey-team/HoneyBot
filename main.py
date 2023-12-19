import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands


bot = commands.Bot()


@bot.event
async def on_ready():
    print('The bot is ready!')


load_dotenv('token.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot.run(BOT_TOKEN)
