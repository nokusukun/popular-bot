from util import Events
import glob
import os
import random
import asyncio


class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.UserJoin("welcome_msg"), Events.UserLeave("leave_msg"), ]

    async def handle_member_join(self, member):
        welcome = glob.glob(os.getcwd() + "/images/" + 'hi.gif')
        file = random.choice(welcome)
        await asyncio.sleep(1)
        await self.pm.client.send_message(member.server.default_channel,
                                          "Welcome to the server " + member.mention +
                                          " Please read <#234865303442423814> and tell an admin/mod which role you would like")
        await self.pm.client.send_file(member.server.default_channel, file)

    async def handle_member_leave(self, member):
        leave = glob.glob(os.getcwd() + "/images/" + "bye.gif")
        file = random.choice(leave)
        await asyncio.sleep(1)
        await self.pm.client.send_message(member.server.default_channel, "Bye " + member.mention)
        await self.pm.client.send_file(member.server.default_channel, file)
