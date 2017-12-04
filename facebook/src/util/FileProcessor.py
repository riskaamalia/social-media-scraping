import json
from os.path import dirname, abspath


class FileProcessor :

    def config (key_name) :
        location = str(dirname(dirname(abspath('config'))))+"/config/file-store-config.json"
        with open(location) as data_file:
            value = json.load(data_file)[key_name]

        return value

    # write to file per line
    def write (path, content) :
        fWrite = open(path, "a")
        with fWrite as myfile:
            myfile.write(content)
            fWrite.close()

    def is_url_exists (path, content) :
        exist = 0
        for check in open(path) :
            if content in check :
                exist = 1
                break

        return exist
