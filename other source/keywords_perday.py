import os
from datetime import datetime

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))
space = " , "
date = str(datetime.now().strftime('%Y-%m-%d'))

def check (source, keyword) :
    location = path + "/config/keywords_perday_" + source + ".log"

    acess_file = open(location,'a+')
    check_read = acess_file.read().splitlines()

    # check total store keywords first, flush if too many
    flush_keywords(source)

    is_exist = False
    for check in check_read :
        if keyword == check.split(space)[1] :
            is_exist = True
            break

    if is_exist == False :
        acess_file.write(date+space+keyword+'\n')

    acess_file.close()

    return is_exist

def flush_keywords (source) :
    location = path + "/config/keywords_perday_" + source + ".log"
    location_keywords = path + "/config/keyword.log"

    access_keywords = open(location_keywords,'r')
    check_keywords = access_keywords.read().splitlines()

    acess_file = open(location, 'r')
    check_read = acess_file.read().splitlines()

    if len(check_read) >= len(check_keywords) :
        flush_file = open(location,'w')
        flush_file.close()

    access_keywords.close()
    acess_file.close()
