from configparser import ConfigParser


class config_app:
    def config_app(self, filename="config/config.ini", section="appConfig"):
        parser = ConfigParser()
        parser.read(filename)

        data = parser[section]
        return data
