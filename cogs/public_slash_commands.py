import disnake
from disnake.ext import commands
from datetime import datetime
import manage_servers_db as manage_db
import utils


class PublicSlashCommands(commands.Cog):
    """This will be for a ping command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Get the bot's current websocket latency."""
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.slash_command()
    async def user_info(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
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
        embed_user_info.add_field(
            name="Joined at", value=member.joined_at.date(), inline=True)
        embed_user_info.add_field(
            name="Created at", value=member._user.created_at.date(), inline=True)
        embed_user_info.add_field(
            name="ID", value=member._user.id, inline=True)

        await inter.response.send_message(embed=embed_user_info)

    @commands.slash_command()
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        """Returns info about server."""
        guild = inter.guild
        moderator_roles_str = ''

        for role_id in manage_db.get_moderator_roles(guild.id):
            moderator_roles_str += guild.get_role(int(role_id)).mention + '\n'

        embed_server_info = disnake.Embed(
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        embed_server_info.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        embed_server_info.set_thumbnail(url=guild.icon.url)

        embed_server_info.add_field(name='Name', value=guild.name, inline=True)
        embed_server_info.add_field(
            name='Description', value=guild.description, inline=True)
        embed_server_info.add_field(
            name='Created at', value=guild.created_at.date(), inline=True)
        embed_server_info.add_field(name='ID', value=guild.id, inline=True)
        embed_server_info.add_field(
            name='Members count', value=guild.member_count, inline=True)
        embed_server_info.add_field(
            name="Moderator's roles", value=moderator_roles_str, inline=True)
        
        await inter.response.send_message(embed=embed_server_info)

    @commands.slash_command()
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
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

    @commands.slash_command()
    # @utils.required_administrator
    async def add_moderator_role(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        """Adds the role to moderator's roles"""
        result_embed = disnake.Embed(
            description=f"{role.mention} was successfully added to moderator's roles.",
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        result_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        if not manage_db.add_moderator_role(inter.guild_id, role.id):
            result_embed.description = f"{role.mention} is already in moderator's roles."

        await inter.response.send_message(embed=result_embed)

    @commands.slash_command()
    # @utils.required_administrator
    async def remove_moderator_role(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        """Removes the role from moderator's roles"""
        result_embed = disnake.Embed(
            description=f"{role.mention} was successfully removed from moderator's roles.",
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        result_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        if not manage_db.remove_moderator_role(inter.guild_id, role.id):
            result_embed.description = f"{role.mention} isn't in moderator's roles."

        await inter.response.send_message(embed=result_embed)


def setup(bot: commands.Bot):
    bot.add_cog(PublicSlashCommands(bot))