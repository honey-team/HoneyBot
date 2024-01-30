import disnake
from disnake.ext import commands
from datetime import datetime
from utils import manage_servers_db as manage_db
from utils import decorators
from utils import modals


class PublicSlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name=disnake.Localized("user_info", key="USER_INFO_COMMAND_NAME"),
        description=disnake.Localized(
            "Returns info about user.", key="USER_INFO_COMMAND_DESCRIPTION")
    )
    async def user_info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            default=None,
            name=disnake.Localized(
                "member", key="USER_INFO_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized(
                "The member, info about that you want to get.", key="USER_INFO_COMMAND_PARAM_MEMBER_DESCRIPTION")
        )
    ):
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

    @commands.slash_command(
        name=disnake.Localized("server_info", key="SERVER_INFO_COMMAND_NAME"),
        description=disnake.Localized(
            "Returns info about server.", key="SERVER_INFO_COMMAND_DESCRIPTION")
    )
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild
        moderator_roles_str = ''
        users = []
        bots = []

        for member in await guild.chunk():
            if member.bot:
                bots.append(member)
            else:
                users.append(member)

        for role_id in manage_db.get_moderator_roles(guild.id):
            moderator_roles_str += guild.get_role(role_id).mention + '\n'

        embed_server_info = disnake.Embed(
            title=f"Information about server {guild.name}",
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        embed_server_info.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        embed_server_info.set_thumbnail(url=guild.icon.url)

        embed_server_info.add_field(
            name='Members:', value=f"All: **{guild.member_count}**\nUsers: **{len(users)}**\nBots: **{len(bots)}**", inline=True)
        embed_server_info.add_field(
            name='Channels:', value=f"All: **{len(guild.channels)}**\nText: **{len(guild.text_channels)}**\nForum: **{len(guild.forum_channels)}**\nVoice: **{len(guild.voice_channels)}**", inline=True)
        embed_server_info.add_field(
            name="Moderator's roles", value=moderator_roles_str, inline=True)
        # embed_server_info.add_field(name='Owner:', value=guild.owner.name, inline=True)
        embed_server_info.add_field(
            name='Created at', value=guild.created_at.date(), inline=True)
        embed_server_info.add_field(name='ID', value=guild.id, inline=True)
        await inter.response.send_message(embed=embed_server_info)

    @commands.slash_command(
        name=disnake.Localized("avatar", key="AVATAR_COMMAND_NAME"),
        description=disnake.Localized(
            "Returns user's avatar.", key="AVATAR_COMMAND_DESCRIPTION")
    )
    async def avatar(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            default=None,
            name=disnake.Localized(
                "member", key="AVATAR_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized(
                "Member, that's avatar you want to get.", key="AVATAR_COMMAND_PARAM_MEMBER_DESCRIPTION")
        )
    ):
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

    @commands.slash_command(
        name=disnake.Localized("send_embed", key="SEND_EMBED_COMMAND_NAME"),
        description=disnake.Localized("Creates the modal window and though it sends embed message.", key="SEND_EMBED_COMMAND_DESCRIPTION")
    )
    async def send_embed(self, inter: disnake.ApplicationCommandInteraction):
        """Sends the embed message."""
        await inter.response.send_modal(modal=modals.CreateEmbedModal())


def setup(bot: commands.Bot):
    bot.add_cog(PublicSlashCommands(bot))
