from configparser import ConfigParser, NoSectionError, NoOptionError


class BotPreferences(object):
    """
    The BotPreferences class manages access to the config.ini file. Plugins can access these settings,
    but new settings have to be added to the file manually.
    """

    # Prefix for commands, this can be changed to prevent issues with other bots in a server.
    # Multiple characters are supported
    commandPrefix = "!"

    # Bot nickname, the bot will use this nickname on startup. Can be temporarily changed with BotNick.py plugin
    nickName = "Popular Bot"

    # Discord API OAuth token, used to login. Needs to be created by the bot owner.
    token = "DEFAULT_TOKEN"

    # Permissions list, each permission level will contain the names of groups that are assigned to it.
    # Ex: Admin: Admin, Owner / Member: Verified / Default: @everyone
    admin = list()
    mod = list()
    member = list()
    default = list()

    def __init__(self):
        """
        Load the config file into memory and read their values
        """
        self.config = ConfigParser()
        self.reload_config()

    def bind_roles(self, name, container):
        """
        This method will read all the (comma separated) roles from the config file and assign them to the specified
        permission level
        :param name: Permission level name in config file
        :param container: Container list to add the groups to
        """
        roles = self.get_config_value(name, "groups").split(",")
        for role in roles:
            container.append(role.strip())

    def reload_config(self):
        """
        Reload the values in the config file into memory
        """
        self.config.read("config")

        # Discord login token
        self.token = self.get_config_value("client", "token")

        # Bot nickname
        self.nickName = self.get_config_value("client", "nick")

        # Command prefix
        self.commandPrefix = self.get_config_value("client", "prefix")

        # Bind roles
        self.bind_roles("Admin", self.admin)
        self.bind_roles("Mod", self.mod) 
        self.bind_roles("Member", self.member)
        self.bind_roles("Default", self.default)

    def get_config_value(self, category, item):
        """
        Method that can be used by plugins to access values in the config file.
        :param category: Config category (ex: "Admin" is for [Admin])
        :param item: Config item in category
        :return: Value as a string
        """
        try:
            return str(self.config.get(category, item))
        except NoSectionError as e:
            print("Can't find section " + e.section)
        except NoOptionError as e:
            print("Can't find option " + e.option + ", " + e.section)
