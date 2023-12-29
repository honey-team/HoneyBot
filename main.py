import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands


bot = commands.Bot(test_guilds=[1113102018991620228, 972183553775382530])


@bot.event
async def on_ready():
    print('The bot is ready!')


# @bot.slash_command(guild_ids=[1113102018991620228])
# async def ping(inter: disnake.ApplicationCommandInteraction):
#     await inter.response.send_message("Pong!")

bot.load_extension("cogs.public_commands")
    
    
# @bot.slash_command()
# async def server_info(inter: disnake.ApplicationCommandInteraction):
#     """Returns the info about the server"""
#     await inter.response.send_message(f"Server name: {inter.guild.name}\nTotal members: {inter.guild.member_count}")


# @bot.slash_command()
# async def user_info(inter: disnake.ApplicationCommandInteraction):
#     """Returns the info about the user"""
#     await inter.response.send_message(f"User name: {inter.author}\nUser ID: {inter.author.id}")


load_dotenv('token.env')

bot.run(os.getenv('BOT_TOKEN'))
