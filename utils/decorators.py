from datetime import datetime
import disnake
import functools
import manage_servers_db as manage_db
from disnake.ext import commands


def required_moderator(func):
    """This decorator only for functions with .slash_command()."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        inter: disnake.ApplicationCommandInteraction = kwargs.get('inter')
        
        moderator_roles = manage_db.get_moderator_roles(guild_id=inter.guild_id)
        for role in inter.author.roles:
            if role.id in moderator_roles:
                return await func(*args, **kwargs)
        
        # raise commands.errors.MissingAnyRole()
        error_embed = disnake.Embed(
            title="You don't have moderator permissions!",
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        error_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        await inter.response.send_message(embed=error_embed)
    
    return wrapper
