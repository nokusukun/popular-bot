from util import Events
from util.Ranks import Ranks
import operator
import discord


class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Command("rolestat", Ranks.Mod,
                               desc="Shows the amount of users in each role"),
                Events.Command("serverinfo", desc="Shows information about the server")]

    async def handle_command(self, message_object, command, args):
        if command == "serverinfo":
            await self.server_info(message_object)
        if command == "rolestat":
            await self.rolestat(message_object)

    async def rolestat(self, message_object):
        server = message_object.server
        msg = "Role stats for this server (" + str(server.member_count) + " users in total):\n"

        roles = dict()

        for member in server.members:
            for member_role in member.roles:
                if member_role.name != "@everyone":
                    if member_role.name in roles:
                        roles[member_role.name] += 1
                    else:
                        roles[member_role.name] = 1
        sorted_x = sorted(roles.items(), key=operator.itemgetter(1))
        for role, count in reversed(sorted_x):
            msg += role + ": " + str(count) + " users\n"

        await self.pm.client.send_message(message_object.channel, msg)

    async def server_info(self, message_object):
        server = message_object.server
        msg = "**Name:** " + server.name + " (" + server.id + ")\n"
        msg += "**Total members:** " + str(server.member_count) + "\n"
        msg += "**Server owner:** " + server.owner.name + "\n"
        msg += "**Server region:** " + str(server.region) + "\n"
        msg += "**Created at:** " + server.created_at.strftime("%B %d, %Y")

        em = discord.Embed(description="Server Icon", colour=0xFFFFFF)
        em.set_image(url=server.icon_url)
        msg = await self.pm.client.send_message(message_object.channel, msg)
        await self.pm.client.edit_message(msg, embed=em)
