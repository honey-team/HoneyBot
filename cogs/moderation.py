import disnake
from disnake.ext import commands
from datetime import datetime
from utils import manage_servers_db as manage_db
from utils import decorators


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


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
