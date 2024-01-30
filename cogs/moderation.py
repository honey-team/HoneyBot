import disnake
from disnake.ext import commands
from datetime import datetime
from datetime import timedelta
from utils import manage_servers_db as manage_db
from utils import decorators
from utils import utils


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name=disnake.Localized("add_moderator_role",
                               key="ADD_MODERATOR_ROLE_COMMAND_NAME"),
        description=disnake.Localized(
            "Adds the role to moderator's roles.", key="ADD_MODERATOR_ROLE_COMMAND_DESCRIPTION")
    )
    @commands.has_guild_permissions(administrator=True)
    async def add_moderator_role(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = commands.Param(
            name=disnake.Localized(
                "role", key="ADD_MODERATOR_ROLE_COMMAND_PARAM_ROLE_NAME"),
            description=disnake.Localized("The role, that's you want to add to moderator's roles.",
                                          key="ADD_MODERATOR_ROLE_COMMAND_PARAM_ROLE_DESCRIPTION")
        )
    ):
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

    @commands.slash_command(
        name=disnake.Localized("remove_moderator_role",
                               key="REMOVE_MODERATOR_ROLE_COMMAND_NAME"),
        description=disnake.Localized(
            "Removes the role from moderator's roles.", key="REMOVE_MODERATOR_ROLE_COMMAND_DESCRIPTION")
    )
    @commands.has_guild_permissions(administrator=True)
    async def remove_moderator_role(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = commands.Param(
            name=disnake.Localized(
                "role", key="REMOVE_MODERATOR_ROLE_COMMAND_PARAM_ROLE_NAME"),
            description=disnake.Localized("The role, that's you want to remove from moderator's roles.",
                                          key="REMOVE_MODERATOR_ROLE_COMMAND_PARAM_ROLE_DESCRIPTION")
        )
    ):
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

    @commands.slash_command(
        name=disnake.Localized("clear", key="CLEAR_COMMAND_NAME"),
        description=disnake.Localized(
            "Removes the messages.", key="CLEAR_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def clear(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name=disnake.Localized(
                "amount", key="CLEAR_COMMAND_PARAM_AMOUNT_NAME"),
            description=disnake.Localized(
                "The amount of messages, thats you want to remove.", key="CLEAR_COMMAND_PARAM_AMOUNT_DESCRIPTION")
        ),
        author: disnake.Member = commands.Param(
            default=None,
            name=disnake.Localized(
                "author", key="CLEAR_COMMAND_PARAM_AUTHOR_NAME"),
            description=disnake.Localized(
                "The author, that's messages you want to remove.", key="CLEAR_COMMAND_PARAM_AUTHOR_DESCRIPTION")
        )
    ):
        def check(m: disnake.Message):
            if author:
                return m.author == author
            return True
        deleted = await inter.channel.purge(limit=amount, check=check)

        messages_deleted_embed = disnake.Embed(
            description=f"Deleted {len(deleted)} messages.",
            color=0xfa7c10,
            timestamp=datetime.now()
        )

        messages_deleted_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        await inter.response.send_message(embed=messages_deleted_embed, delete_after=10)
    
    @commands.slash_command(
        name=disnake.Localized("mute", key="MUTE_COMMAND_NAME"),
        description=disnake.Localized("Mutes the member.", key="MUTE_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def mute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="MUTE_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized("The member, that you want to mute.", key="MUTE_COMMAND_PARAM_MEMBER_DESCRIPTION")
        ),
        duration: str = commands.Param(
            name=disnake.Localized("duration", key="MUTE_COMMAND_PARAM_DURATION_NAME"),
            description=disnake.Localized("The duration, for that you want to mute the member, takes time as: '3d', '1h', '17m', '32s'.", key="MUTE_COMMAND_PARAM_DURATION_DESCRIPTION")
        ),
        reason: str = commands.Param(
            default=None,
            name=disnake.Localized("reason", key="MUTE_COMMAND_PARAM_REASON_NAME"),
            description=disnake.Localized("The reason, for that you want to mute the member.", key="MUTE_COMMAND_PARAM_REASON_DESCRIPTION")
        )
    ):
        mute_embed = disnake.Embed(
            description=f'{member.mention} was succesfully muted for {duration} for reason: "{reason}"',
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        mute_embed.set_thumbnail(url=member.avatar.url)

        mute_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        await member.timeout(duration=utils.from_str_to_timedelta(duration), reason=reason)
        await inter.response.send_message(embed=mute_embed)
    
    @commands.slash_command(
        name=disnake.Localized("unmute", key="UNMUTE_COMMAND_NAME"),
        description=disnake.Localized("Unmutes the member.", key="UNMUTE_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def unmute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="UNMUTE_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized("The member, that you want to unmute.", key="UNMUTE_COMMAND_PARAM_MEMBER_DESCRIPTION")
        ),
        reason: str = commands.Param(
            default=None,
            name=disnake.Localized("reason", key="UNMUTE_COMMAND_PARAM_REASON_NAME"),
            description=disnake.Localized("The reason, for that you want to unmute the member.", key="UNMUTE_COMMAND_PARAM_REASON_DESCRIPTION")
        )
    ):
        unmute_embed = disnake.Embed(
            description=f'{member.mention} was succesfully unmuted for reason: "{reason}"',
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        unmute_embed.set_thumbnail(url=member.avatar.url)

        unmute_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        await member.timeout(duration=None, reason=reason)
        await inter.response.send_message(embed=unmute_embed)
    
    @commands.slash_command(
        name=disnake.Localized("kick", key="KICK_COMMAND_NAME"),
        description=disnake.Localized("Kicks the member.", key="KICK_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def kick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="KICK_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized("The member, that you want to kick.", key="KICK_COMMAND_PARAM_MEMBER_DESCRIPTION")
        ),
        reason: str = commands.Param(
            default=None,
            name=disnake.Localized("reason", key="KICK_COMMAND_PARAM_REASON_NAME"),
            description=disnake.Localized("The reason, for that you want to kick the member.", key="KICK_COMMAND_PARAM_REASON_DESCRIPTION")
        )
    ):
        kick_embed = disnake.Embed(
            description=f'{member.mention} was succesfully kicked for reason: "{reason}"',
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        kick_embed.set_thumbnail(url=member.avatar.url)

        kick_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        await member.kick(reason=reason)
        await inter.response.send_message(embed=kick_embed)
    
    @commands.slash_command(
        name=disnake.Localized("ban", key="BAN_COMMAND_NAME"),
        description=disnake.Localized("Bans the member.", key="BAN_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="BAN_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized("The member, that you want to ban.", key="BAN_COMMAND_PARAM_MEMBER_DESCRIPTION")
        ),
        reason: str = commands.Param(
            default=None,
            name=disnake.Localized("reason", key="BAN_COMMAND_PARAM_REASON_NAME"),
            description=disnake.Localized("The reason, for that you want to ban the member.", key="BAN_COMMAND_PARAM_REASON_DESCRIPTION")
        )
    ):
        ban_embed = disnake.Embed(
            description=f'{member.mention} was succesfully banned for reason: "{reason}"',
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        ban_embed.set_thumbnail(url=member.avatar.url)

        ban_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        await member.ban(reason=reason)
        await inter.response.send_message(embed=ban_embed)
    
    @commands.slash_command(
        name=disnake.Localized("unban", key="UNBAN_COMMAND_NAME"),
        description=disnake.Localized("Unbans the member.", key="UNBAN_COMMAND_DESCRIPTION")
    )
    @decorators.required_moderator
    async def unban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="UNBAN_COMMAND_PARAM_MEMBER_NAME"),
            description=disnake.Localized("The member, that you want to unban.", key="UNBAN_COMMAND_PARAM_MEMBER_DESCRIPTION")
        ),
        reason: str = commands.Param(
            default=None,
            name=disnake.Localized("reason", key="UN_COMMAND_PARAM_REASON_NAME"),
            description=disnake.Localized("The reason, for that you want to unban the member.", key="UNBAN_COMMAND_PARAM_REASON_DESCRIPTION")
        )
    ):
        unban_embed = disnake.Embed(
            description=f'{member.mention} was succesfully unbanned for reason: "{reason}"',
            color=0xfa7c10,
            timestamp=datetime.now()
        )
        
        unban_embed.set_thumbnail(url=member.avatar.url)

        unban_embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        await member.unban(reason=reason)
        await inter.response.send_message(embed=unban_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
