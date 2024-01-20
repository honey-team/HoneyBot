import disnake
from disnake.ext import commands
import sqlite3


def create_servers_db():
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Servers (
                       guild_id INTEGER NOT NULL,
                       moderator_roles TEXT
                   )
                   ''')


def get_command_prefix(bot: commands.Bot, message: disnake.Message):
    """Gets command prefix from db."""
    # ! This function is useless, because I don't wanna add prefix commands.
    return '!'


async def add_server(guild_id: int):
    """Adds server to db."""
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Servers (guild_id) VALUES (?)", (guild_id,))


async def remove_server(guild_id: int):
    """Removes server from db."""
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Servers WHERE guild_id = ?", (guild_id,))


def add_moderator_role(guild_id: int, role_id: int) -> bool:
    """Adds moderator role to the server from db."""
    role_id = str(role_id)
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT moderator_roles FROM Servers WHERE guild_id = ?", (guild_id,))
        moderator_roles_str = cursor.fetchall()[0][0]
        moderator_roles_list: list = []
        if moderator_roles_str:
            moderator_roles_list = moderator_roles_str.split('/')
            if role_id in moderator_roles_list:
                return False

            moderator_roles_list.append(role_id)
            moderator_roles_str = "/".join(moderator_roles_list)
        else:
            moderator_roles_list.append(role_id)
            moderator_roles_str = "/".join(moderator_roles_list)

        cursor.execute("UPDATE Servers SET moderator_roles = ? WHERE guild_id = ?",
                       (moderator_roles_str, guild_id))
        return True


def remove_moderator_role(guild_id: int, role_id: int) -> bool:
    """Removes moderator role from the server from db."""
    role_id = str(role_id)
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT moderator_roles FROM Servers WHERE guild_id = ?", (guild_id,))
        moderator_roles_str = cursor.fetchall()[0][0]
        moderator_roles_list: list = []
        if moderator_roles_str:
            moderator_roles_list = moderator_roles_str.split('/')
            if role_id not in moderator_roles_list:
                return False

            moderator_roles_list.remove(role_id)
            moderator_roles_str = "/".join(moderator_roles_list)
        else:
            return False

        cursor.execute("UPDATE Servers SET moderator_roles = ? WHERE guild_id = ?",
                       (moderator_roles_str, guild_id))
        return True


def get_moderator_roles(guild_id: int) -> list:
    """Gets moderator's roles."""
    with sqlite3.connect("servers.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT moderator_roles FROM Servers WHERE guild_id = ?", (guild_id,))
        moderator_roles_str = cursor.fetchall()[0][0]
        moderator_roles_list = []
        for str_role_id in moderator_roles_str.split("/"):
            moderator_roles_list.append(int(str_role_id))

        return moderator_roles_list


async def check_moderator_role(guild_id: int, role_id: int) -> bool:
    """Checks are role is moderator role."""
    pass


if __name__ == "__main__":
    create_servers_db()
