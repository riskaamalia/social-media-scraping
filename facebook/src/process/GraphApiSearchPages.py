import logging
from util.UrlProcessor import UrlProcessor
from time import sleep


def processor (dao,keyword,token,limit) :
    for kw in keyword :
        logging.info("Processing finds pages from queries with keyword : "+kw)
        execute_process_to_db(kw.replace(" ","%20"),dao,token,limit)
        logging.info('sleep for a while in 300 seconds')
        sleep(300)
    logging.info('sleep in 10 minutes for regenerate page ....')
    sleep(600)

def execute_process_to_db (keyword, dao, token, limit) :

    base_url = "https://graph.facebook.com/v2.10/search?access_token="+token+"&fields=link&type=page&limit="+str(limit)+"&q="
    url = base_url+keyword
    get_body = UrlProcessor().get_json_body(url)
    while get_body is not None :
        try :
            json_body = get_body['data']
            # print(json_body)

            total_write = 0
            for data in json_body :
                row=[data['link'],keyword]

                # insert into db
                try :
                    if dao.is_url_page_exist(data['link']) == 0 :
                        dao.add_page(row)
                        total_write=total_write+1
                        logging.info("Write : "+data['link']+" total write : "+str(total_write))
                except Exception as e :
                    logging.exception(str(e.message)[0:10])

            get_paging = get_body['paging']
            logging.info("Go to next page")
            url = get_paging['next']
            get_body = UrlProcessor().get_json_body(url)
        except Exception as e:
            logging.info(str(e.message))
            get_body = None

