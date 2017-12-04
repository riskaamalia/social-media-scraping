import json
from os.path import dirname, abspath


class ConfigProcessor :

    # write to file per line
    def write_to_file (path, content) :
        fWrite = open(path, "a")
        with fWrite as myfile:
            myfile.write(content)
            fWrite.close()

    def is_url_exists_in_file (path, content) :
        exist = 0
        for check in open(path) :
            if content in check :
                exist = 1
                break

        return exist

    def config_file_storage (key_name) :
        location = str(dirname(dirname(abspath('config'))))+"/config/file-store-config.json"
        with open(location) as data_file:
            value = json.load(data_file)[key_name]

        return value

    # get username and password for facebook log in
    def config_facebook_username (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/facebook-user.json"
        with open(location) as data_file:
            value = json.load(data_file)['username']

        return value

    def config_facebook_password (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/facebook-user.json"
        with open(location) as data_file:
            value = json.load(data_file)['password']

        return value

    # get keyword from config file , this is an array
    def config_facebook_keyword (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/facebook-keyword.json"
        with open(location) as data_file:
            value = json.load(data_file)['keyword']

        return value

    # get value from sqlite
    def config_sqlite (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/sqlite-config.json"
        with open(location) as data_file:
            value = json.load(data_file)['list_config']

        return value

    # get driver configuration
    def config_driver_browser (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/driver-browser.json"
        with open(location) as data_file:
            value = json.load(data_file)['driver_location']

        return value

    # get log name
    def config_log_name (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/logging.json"
        with open(location) as data_file:
            value = json.load(data_file)['project_name']

        return value

    # get log location
    def config_log_location (self) :
        location = str(dirname(dirname(abspath('config'))))+"/config/logging.json"
        with open(location) as data_file:
            value = json.load(data_file)['log_location']

        return value
