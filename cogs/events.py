import disnake
from disnake.ext import commands
from datetime import datetime
import manage_servers_db as manage_db


class Events(commands.Cog):
    def __init___(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('The bot is ready!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        await manage_db.add_server(guild.id)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: disnake.Guild):
        await manage_db.remove_server(guild.id)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        error_embed = disnake.Embed(
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        error_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        if isinstance(error, commands.errors.MissingPermissions):
            if 'administrator' in error.missing_permissions:
                error_embed.title = "You don't have administrator permissions!"
                await inter.response.send_message(embed=error_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))