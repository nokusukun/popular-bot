from util.Ranks import Ranks

"""
The util.Events module describes the supported types of events to which plugins can react. Their signature is the same,
they are identified by their name. These classes don't do anything on their own, they just contain data.
"""


class Command(object):
    """
    Command event, fires when a command is issued in chat
    """

    def __init__(self, name, rank=Ranks.Default, desc=""):
        self.name = name
        self.minimum_rank = rank
        self.desc = desc


class Message(object):
    """
    Message event, fires when a message is posted in chat
    """

    def __init__(self, name, rank=Ranks.Default, desc=""):
        self.name = name
        self.minimum_rank = rank
        self.desc = desc


class BotMention(object):
    """
    BotMention event, fires when the bot gets mentioned
    """

    def __init__(self, name, rank=Ranks.Default, desc=""):
        self.name = name
        self.minimum_rank = rank
        self.desc = desc


class UserJoin(Command):
    """
    UserJoin event, fires when a user joins a server
    NOT IMPLEMENTED
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank


class UserLeave(object):
    """
    UserLeave event, fires when a user leaves a server
    NOT IMPLEMENTED
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank


class BotJoin(object):
    """
    BotJoin event, fires when the bot joins the server
    NOT IMPLEMENTED
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank


class MessageDelete(object):
    """
    MessageDelete event, fires when a message is deleted
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank


class MessageEdit(object):
    """
    MessageEdit event, fires when a message is edited
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank


class Typing(object):
    """
    Typing event, fires when a user is typing in chat
    """

    def __init__(self, name, rank=Ranks.Default):
        self.name = name
        self.minimum_rank = rank
