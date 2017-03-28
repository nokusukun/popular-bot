from util import Events
from util.Ranks import Ranks
import glob
import os
import random
import asyncio
from uuid import uuid4
import aiohttp
import discord
import urllib.request
from uuid import uuid4
import requests
import requests.auth
import urllib
from lxml import html
import praw

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm
        with open("subreddit.db") as f:
            self.subreddits = eval(f.read())
        self.blocked = ["r/the_donald",
            "r/uncensorednews",
            "r/sandersforpresident",
            "r/impeach_trump",
            "r/enoughtrumpspam",
            "r/hillaryforprison",
            "r/marchofempires"]
        self.reddit =  reddit = praw.Reddit(client_id="r7r6bX1KP4lKJQ", client_secret="NHOCyYy3QV6_Gg-GZX07K87G_yg", user_agent="/r/popularmods")



    @staticmethod
    def register_events():
        #Events.UserJoin("authorization"),
        return [Events.UserJoin("authorization"),
        Events.Command("verify", Ranks.Default, ""),
        Events.Command("reverify", Ranks.Admin, "")]

    async def handle_command(self, message_object, command, args):
        if command == "verify":
            await self.verify(message_object.author)
        if command == "reverify":
            await self.verify(message_object.mentions[0])


    async def handle_member_join(self, member):
        print("{0} Joined. Sending verification procedures.".format(member.name))
        await self.verify(member)
        #auth = make_authorization_url(member.id) #Creates authorization URL
        #message = "To join the server, you must first verify your reddit account(No worries, I will only have access to your username).\n{0}".format(auth)
        #self.pm.authorization[member.id] = "!pending" #flags account as pending, also functions as sate checking for the authorization.
        #if "username" in self.pm.authorization[member.id]:
        #    self.pm.authorization[member.id] = "!pending"
        #else:
        #    self.pm.authorization[member.id] = {"username" : "!pending"}
        #await self.pm.client.send_message(member, message)

        #really bad implementation but /shrug
        #waits for the user to authenticate, will be handled by the callback function in the webserver
        #while self.pm.authorization[member.id] == "!pending":
        #    await asyncio.sleep(3)

        #await self.pm.client.send_message(member, "Just verified your account, your username is: {0}".format(self.pm.authorization[member.id][username]))



    async def verify(self, author):
        roles = {"10m" : discord.utils.get(author.server.roles, name="10 Million Subscribers"),
        "5m" : discord.utils.get(author.server.roles, name="5 Million Subscribers"),
        "1m" : discord.utils.get(author.server.roles, name="1 Million Subscribers"),
        "500k" : discord.utils.get(author.server.roles, name="500 Thousand Subscribers"),
        "verify" : discord.utils.get(author.server.roles, name="Verified")
        }
        print("Verify command invoked.")

        arr = False
        while not arr:
            arr = True
            for role in author.roles:
                if role in list(roles.values()):
                    print("[ROLES]Removing {0}".format(role.name))
                    await self.pm.client.remove_roles(author, role)
                    arr = False

        auth = self.make_authorization_url(author.id) #Creates authorization URL
        message = "Welcome to the Popular Mods Discord server!\nTo join the server,visit this link to verify your reddit account(No worries, I will only have access to your username).\n\n{0}".format(auth)

        #if "username" in self.pm.authorization[author.id]:
        #    self.pm.authorization[author.id]["username"] = "!pending" #flags account as pending, also functions as sate checking for the authorization.
        #else:
        self.pm.authorization[author.id] = {"username" : "!pending"}
        await self.pm.client.send_message(author, message)

        #really bad implementation but /shrug
        #waits for the user to authenticate, will be handled by the callback function in the webserver
        while self.pm.authorization[author.id]["username"] == "!pending":
            if self.pm.authorization[author.id]["username"] == "!error":
                return
            await asyncio.sleep(3)

        subs = await self.getSubreddits(self.pm.authorization[author.id]["username"])
        self.pm.authorization[author.id]["subreddits"] = []
        most_sub = 0
        blocked = False
        extraRole = None
        noSub = False
        for usersub in subs:
            print("User Mods: {0}".format(usersub))
        if len(subs) == 0:
            noSub = True
        else:
            most_sub = self.reddit.subreddit(subs[0].split("/")[1]).subscribers

        for usersub in subs:
            if usersub.lower() in self.blocked:
                blocked = True
                #if most_sub < self.subreddits[usersub]:
                #    most_sub = self.subreddits[usersub]
                #self.pm.authorization[author.id]["subreddits"].append(usersub)
                print("--User is moderator of {0}".format(usersub))



        if not blocked and not noSub and most_sub > 1000:
            #print("---User Max Sub Count is {0}".format(most_sub))
            #if most_sub >= 10000000:
            #    extraRole = roles["10m"]
            #elif most_sub >= 5000000:
            #    extraRole = roles["5m"]
            #elif most_sub >= 1000000:
            #    extraRole = roles["1m"]
            #elif most_sub >= 500000:
            #    extraRole = roles["500k"]

            arr = True
            while arr:
                for role in author.roles:
                    if role.name == "Verified":
                        arr = False
                if arr == True:
                    print("---Setting Verified Role")
                    await self.pm.client.add_roles(author, discord.utils.get(author.server.roles, name="Verified"))

            #if extraRole != None:
            #    arr = True
            #    while arr:
            #        for role in author.roles:
            #            if role == extraRole:
            #                arr = False
            #        if arr == True:
            #            print("- -Adding extra role")
            #            await self.pm.client.add_roles(author, extraRole)
                

            await self.pm.client.send_message(author, "Your account: **{0}** is now verified.".format(self.pm.authorization[author.id]["username"]))
            await self.pm.client.change_nickname(author, self.pm.authorization[author.id]["username"])
        elif noSub:
            await self.pm.client.send_message(author, "Your account: **{0}** does not moderate any subreddits.".format(self.pm.authorization[author.id]["username"]))
        elif most_sub < 1000:
            await self.pm.client.send_message(author, "Your account: **{0}** doesn't moderate a subredit with more than 1000 subscribers.".format(self.pm.authorization[author.id]["username"]))
        else:
            await self.pm.client.send_message(author, "Your account: **{0}** is a moderator for one of the blocked subreddits.".format(self.pm.authorization[author.id]["username"]))

    def make_authorization_url(self, user_id):
        # Generate a random string for the state parameter
        # Save it for use later to prevent xsrf attacks
        state = user_id
        params = {"client_id": self.pm.CLIENT_ID,
                  "response_type": "code",
                  "state": state,
                  "redirect_uri": self.pm.REDIRECT_URI,
                  "duration": "temporary",
                  "scope": "identity"}
        url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
        return url

    async def getSubreddits(self, username):
        await asyncio.sleep(10)
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"}
        page = requests.get('http://reddit.com/u/{0}'.format(username), headers=headers)
        #print(page.content)
        tree = html.fromstring(page.content)
        xlist = tree.xpath("//*[@id='side-mod-list']/li")
        print(" ".join([x.xpath("a/text()")[0] for x in xlist]))
        return [x.xpath("a/text()")[0] for x in xlist]