import disnake
from disnake.ext import commands
from datetime import datetime


class PublicCommands(commands.Cog):
    """This will be for a ping command."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Get the bot's current websocket latency."""
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")
        
    @commands.slash_command()
    async def user_info(self, inter: disnake.ApplicationCommandInteraction, *, member: disnake.Member = None):
        """Returns user info."""
        member = inter.author if not member else member
        nick = member.global_name if not member.nick else member.nick
        
        embed_user_info = disnake.Embed(
            color=member.color,
            timestamp=datetime.now()
        )
        
        embed_user_info.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        embed_user_info.set_thumbnail(url=member.avatar.url)
        
        embed_user_info.add_field(name="Name", value=member.name, inline=True)
        embed_user_info.add_field(name="Nick", value=nick, inline=True)
        embed_user_info.add_field(name="Joined at", value=member.joined_at.date(), inline=True)
        embed_user_info.add_field(name="Created at", value=member._user.created_at.date(), inline=True)
        embed_user_info.add_field(name="ID", value=member._user.id, inline=True)
        
        await inter.response.send_message(embed=embed_user_info)
    
    @commands.slash_command()
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, *, member: disnake.Member = None):
        """Returns user's avatar."""
        member = inter.author if not member else member
        
        embed_users_avatar = disnake.Embed(
            title=f"Avatar {member.name}",
            color=member.color,
            timestamp=datetime.now()
        )
        
        embed_users_avatar.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        embed_users_avatar.set_image(member._user.avatar.url)
        
        await inter.response.send_message(embed=embed_users_avatar)

def setup(bot: commands.Bot):
    bot.add_cog(PublicCommands(bot))