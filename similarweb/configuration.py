import os

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))

def get_api_key_and_country () :
    location = path + "/src/sea_similarweb/config/api_key.log"
    f = open(location, 'r')
    value = f.read().splitlines()

    return value