import json
import os

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
parent2 = os.path.abspath(os.path.join(parent1, os.pardir))
parent3 = os.path.abspath(os.path.join(parent2, os.pardir))
path = os.path.abspath(os.path.join(parent3, os.pardir))


class ConfigProcessor :

    # get username and password for facebook log in
    def config_facebook_username (self,country) :
        if country == 'id' :
            location = str(path)+"/src/sea_facebook/config/facebook-user.json"
        else :
            location = str(path) + "/src/sea_facebook/config/facebook-user-malaysia.json"
        with open(location) as data_file:
            value = json.load(data_file)['username']

        return value

    def config_facebook_password (self,country) :
        if country == 'id' :
            location = str(path)+"/src/sea_facebook/config/facebook-user.json"
        else :
            location = str(path) + "/src/sea_facebook/config/facebook-user-malaysia.json"
        with open(location) as data_file:
            value = json.load(data_file)['password']

        return value

    # get keyword from config file , this is an array
    def config_facebook_keyword (self) :
        location = str(path)+"/config/keyword.log"
        f = open(location,'r')
        value = f.read().splitlines()

        return value

    # get keyword from config file for video
    def config_video_keyword (self) :
        location = str(path)+"/config/keyword_video.log"
        f = open(location,'r')
        value = f.read().splitlines()

        return value

    # get value from sql
    def config_sql (self) :
        location = str(path)+"/src/sea_facebook/config/sql-config.json"
        with open(location) as data_file:
            value = json.load(data_file)['list_config']

        return value

    # get driver configuration
    def config_driver_browser (self) :
        location = str(path)+"/src/sea_facebook/config/driver-browser.json"
        with open(location) as data_file:
            value = json.load(data_file)['driver_location']

        return value

    # get log name
    def config_log_name (self) :
        location = str(path)+"/src/sea_facebook/config/logging.json"
        with open(location) as data_file:
            value = json.load(data_file)['project_name']

        return value

    # get log location
    def config_log_location (self) :
        location = str(path)+"/src/sea_facebook/config/logging.json"
        with open(location) as data_file:
            value = json.load(data_file)['log_location']

        return value

    # get loop total
    def config_loop (self) :
        location = str(path)+"/src/sea_facebook/config/loop-config.json"
        with open(location) as data_file:
            value = json.load(data_file)['total_loop']

        return value

    # get facebook token
    def facebook_token (self,key_name,country) :
        if country == 'my' :
            location = str(path)+"/src/sea_facebook/config/facebook-graph-api-malaysia.json"
        elif country == 'th' :
            location = str(path)+"/src/sea_facebook/config/facebook-graph-api-thailand.json"
        elif country == 'vn' :
            location = str(path)+"/src/sea_facebook/config/facebook-graph-api-vietnam.json"
        else :
            location = str(path) + "/src/sea_facebook/config/facebook-graph-api.json"

        with open(location) as data_file:
            value = json.load(data_file)[key_name]

        return value
