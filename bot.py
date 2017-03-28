from PluginManager import PluginManager
import discord
import traceback
from os import environ
from flask import Flask, render_template, send_from_directory, abort, request
import _thread
import time
import socket
import urllib.request
from uuid import uuid4
import requests
import requests.auth
import urllib
import config

# Prelimenary stuff for setting reddit integration settings
CLIENT_ID = config.REDDIT_ID
CLIENT_SECRET = config.REDDIT_SECRET
REDIRECT_URI = config.CALLBACK_URL



print("This bot is running on Nokubot-Heroku Framework!")
print("Initalizing popular-bot F...")
# Creates a discord client, which we will use to connect and interact with the server.
# All methods with @client.event annotations are event handlers for this client.
client = discord.Client()

print("Loading Modules")
# Loads and initializes the plugin manager for the bot
pm = PluginManager("plugins", client)
pm.load_plugins()
pm.register_events()
pm.CLIENT_ID = CLIENT_ID
pm.CLIENT_SECRET = CLIENT_SECRET
pm.REDIRECT_URI = REDIRECT_URI

# Parses the popular.txt file and loads to list
with open("popular.txt") as f:
    pm.POPULAR_SUBS = f.read().splitlines()

print("Plugins loaded and registered")

# Web server in which to do callback stuff for reddit oauth
app = Flask(__name__, static_url_path='')
@app.route("/")
def main():
    #return render_template('index.html', active_users=str(len(get_online_users(60))), users_table=generate_table(), commits=generate_commit())
    #return "Nokusu is online! :3\n There are {0} active users for the past hour.".format()
    return "The bot is online"

@app.route('/pluginsconfig/<path:path>')
def send_config(path):
    return send_from_directory('pluginsconfig', path)

def dummy():
    #port = int(environ.get('PORT'))
    port = 80
    app.run(host='127.0.0.1', port=port)


def ping():
    while True:
        socket.setdefaulttimeout( 23 )  # timeout in seconds
        url = 'https://popular-bot.herokuapp.com/'
        f = urllib.request.urlopen(url)
        x = f.read()
        time.sleep(120)

#Auth webserv stuff
def user_agent():
    return "popular-bot-auth /u/artemize"

def base_headers():
    return {"User-Agent": user_agent()}

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

def save_created_state(state):
    pass
def is_valid_state(state):
    return True


@app.route('/callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get("code")
    user_id = request.args.get("state")
    access_token = get_token(code)
    username = get_username(access_token)
    pm.authorization[user_id]["username"] = username
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your reddit username is: {0}. Please wait for the bot to finish verifying your account. You may now close this window.".format(username)

def get_token(code):
    time.sleep(2)
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"})
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]
    
    
def get_username(access_token):
    time.sleep(2)
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token,
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']


#Discord Bot stuff below

@client.event
async def on_ready():
    """
    Event handler, fires when the bot has connected and is logged in
    """
    print('Logged in as ' + client.user.name + " (" + client.user.id + ")")

    # Change nickname to nickname in configuration
    for instance in client.servers:
        await client.change_nickname(instance.me, pm.botPreferences.nickName)
    await client.change_presence(game=discord.Game(name='Under Construction'))


@client.event
async def on_message(message):
    """
    Event handler, fires when a message is received in the server.
    :param message: discord.Message object containing the received message
    """
    try:
        if message.content.startswith(pm.botPreferences.commandPrefix):
            # Send the received message off to the Plugin Manager to handle the command
            words = message.content.partition(' ')
            await pm.handle_command(message, words[0][len(pm.botPreferences.commandPrefix):], words[1:])
        else:
            await pm.handle_message(message)
    except Exception as e:
        await client.send_message(message.channel, "Error: " + str(e))
        if pm.botPreferences.get_config_value("client", "debug") == "1":
            traceback.print_exc()


@client.event
async def on_typing(channel, user, when):
    """
    Event handler, fires when a user is typing in a channel
    :param channel: discord.Channel object containing channel information
    :param user: discord.Member object containing the user information
    :param when: datetime timestamp
    """
    try:
        await pm.handle_typing(channel, user, when)
    except Exception as e:
        await client.send_message(channel, "Error: " + str(e))
        if pm.botPreferences.get_config_value("client", "debug") == "1":
            traceback.print_exc()


@client.event
async def on_message_delete(message):
    """
    Event handler, fires when a message is deleted
    :param message: discord.Message object containing the deleted message
    """
    try:
        if message.author.name != "PluginBot":
            await pm.handle_message_delete(message)
    except Exception as e:
        await client.send_message(message.channel, "Error: " + str(e))
        if pm.botPreferences.get_config_value("client", "debug") == "1":
            traceback.print_exc()


@client.event
async def on_member_join(member):
    await pm.handle_member_join(member)


@client.event
async def on_member_remove(member):
    await pm.handle_member_leave(member)

# Run web server and keep-alive daemons
print("Running Dummy Server")
_thread.start_new_thread( dummy , ())
print("Dummy Server is Running")
print("Running Heartbeat Service")
#_thread.start_new_thread( ping , ())
print("Heartbeat Service is Running")
# Run the client and login with the bot token (yes, this needs to be down here)
client.run(pm.botPreferences.token)
