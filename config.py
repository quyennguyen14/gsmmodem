from configparser import ConfigParser


class config_app:
    def config_app(self, filename="config.ini", section="appConfig"):
        parser = ConfigParser()
        parser.read(filename)

        data = parser[section]
        return data

    def config_api(self, filename="config.ini", section="apiConfig"):
        parser = ConfigParser()
        parser.read(filename)

        data = parser[section]
        return data

    def config_mysql(self, filename="config.ini", section="mysql"):
        parser = ConfigParser()
        parser.read(filename)

        data = parser[section]
        return data

#  configInfo = config_app()
#  resutl = configInfo.config_app()
#  print(resutl["port"])
