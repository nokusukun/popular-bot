from util import Events
from tinydb import TinyDB, where, Query
from util.Ranks import Ranks

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm
        #self.macroPath = 'pluginsconfig/static_help_data.json'
        #self.macroDB = TinyDB(self.macroPath)

    @staticmethod
    def register_events():
        return [Events.Command("help"), 
        Events.Command("sys.info"),
        Events.Command("help.add", Ranks.Admin),
        Events.Command("help.delete", Ranks.Admin),
        Events.Command("?"),
        Events.Command("hello")]

    async def handle_command(self, message_object, command, args):
        if command == "help":
            if "all" in args[1]:
                await self.allHelp(message_object)
            else:
                await self.helpShowAssigned(message_object)
        if command == "sys.info":
            await self.info(message_object)
        if command == "hello":
            await self.hello(message_object)
        elif command == "help.add":
            await self.helpadd(message_object, args[1])
        elif command == "help.delete":
            await self.helpdel(message_object, args[1])
        elif command == "?":
            await self.helpShow(message_object, args[1])

    async def allHelp(self, message_object):
        hstr = "Nokubot Complete Command List\n"
        for name, commands in self.pm.comlist.items():
            hstr = hstr + "\nModule: **{0}**\n```List:\n".format(name[:-3])
            for c, d in commands:
                hstr = hstr + "~" + c + ": " + d + "\n"
            hstr = hstr + "```"
            await self.pm.client.send_message(message_object.channel, hstr)
            hstr = ""
        #print(hstr)
        

    async def help(self, message_object):
        await self.pm.client.send_message(message_object.channel, 'Noku Bot is still in development! Contact @Noku for more info. :3')
        await self.pm.client.send_message(message_object.channel, '```---There\'s two modules available---\n~help.game\n~help.util```')

    async def info(self, message_object):
        await self.pm.client.send_message(message_object.channel, '`Noku Bot Version ??? IDK what to put here yet`')

    async def hello(self, message_object):
        msg = 'Hello {0.author.mention}'.format(message_object)
        await self.pm.client.send_message(message_object.channel, msg)

    async def helpShow(self, message_object, args):
        try:
            try:
                hstr = "Help for module: **{0}**\nList:\n".format(args)
                for c, d in self.pm.comlist[args+".py"]:
                    hstr = hstr + "`~" + c + "`: " + d + "\n"
                hstr = hstr + "```"
                await self.pm.client.send_message(message_object.channel, hstr)
            except:
                await self.pm.client.send_message(message_object.channel, self.macroDB.search(Query().trigger == args)[0]["data"])
        except:
            await self.pm.client.send_message(message_object.channel, ":exclamation:`Welp, that\'s not a valid help topic!`")

    async def helpShowAssigned(self, message_object):

        for name, commands in self.pm.comlist.items():
            x = x + name[:-3] + " "

        x = x + "```\n`~? [help_topic]` to evoke a help topic.\n`~help all` for all commands."
        await self.pm.client.send_message(message_object.channel, x)

    async def helpadd(self, message_object, args):
        trigger = args.split(" ")[0]
        self.macroDB.insert({'trigger' : trigger, 'data' : args[len(trigger):]})
        await self.pm.client.send_message(message_object.channel, ":information_source:`{0} has been added as a macro!`".format(trigger))

    async def helpdel(self, message_object, args):
        self.macroDB.remove(Query().trigger == args)
        await self.pm.client.send_message(message_object.channel, ":information_source:`{0} has been deleted! Probably..`".format(args))
