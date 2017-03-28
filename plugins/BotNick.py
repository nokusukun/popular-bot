from util import Events
from util.Ranks import Ranks


class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Command("nick", Ranks.Admin,
                               desc="Change the nickname for the bot. Admin only")]

    async def handle_command(self, message_object, command, args):
        if command == "nick":
            await self.nick(message_object, args[1])

    async def nick(self, message_object, nick):
        await self.pm.client.change_nickname(message_object.server.me, nick)
