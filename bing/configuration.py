import os

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))

def get_keywords () :
        location = path + "/config/keyword.log"
        f = open(location,'r')
        value = f.read().splitlines()

        return value

