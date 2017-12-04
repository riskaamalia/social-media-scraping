import logging
import sys
import glob, os
from openpyxl import load_workbook

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_libr import sea_check
from sea_utils import common_utils

common_utils.setup_logging('similarweb.log')

def store_id_file (id) :
    location = dir_path+'/src/sample/data_file.txt'
    data_file = open(location, 'w')
    data_file.write(id)
    data_file.close()

def get_id_file () :
    location = dir_path+'/src/sample/data_file.txt'
    data_file = open(location, 'r')
    get_id = data_file.read()
    data_file.close()

    return get_id

# @timeout_decorator.timeout(30, use_signals=True,exception_message='reach timeout ....')
def is_exist (url,keyword) :
    logging.info (sea_check.is_exist('http://' + url, 'similarweb', keyword))

dir_path = os.path.abspath(os.path.join(dir_path,os.pardir))
location = dir_path+"/config/similarweb/similarweb/"
os.chdir(location)

id_from_file = get_id_file()
if id_from_file != '' :
    last_file = int(id_from_file)
else :
    last_file = 0

big_loop = 1
logging.info ('total file : '+str(len(glob.glob("*.xlsx"))))
for file in glob.glob("*.xlsx"):
    count_exception = 0
    try :
        logging.info (str(big_loop)+'.) FILE name : '+file)
        wb = load_workbook(location+file)
        sheet_ranges = wb['Report Details']
        keyword = str(sheet_ranges['E6'].value).lower()
        logging.info ('keyword : '+keyword)
        sheet_url = wb['Aggregated Data for Time Period']
        loop = 2
        url_start = str(sheet_url['A'+str(loop)].value).lower()
        is_run = True
        while is_run == True and loop > last_file :
            try :
                logging.info (str(loop)+'.) '+url_start)
                is_exist(url_start,keyword.lower())
                url_start = str(sheet_url['A'+str(loop)].value).lower()
                count_exception = 0
            except Exception as e :
                logging.exception (str(e.message))
                count_exception = count_exception + 1
                if count_exception > 5 :
                    store_id_file(big_loop)
                    is_run = False
            loop = loop + 1
    except Exception as e :
        logging.exception (str(e.message))
    big_loop = big_loop + 1


