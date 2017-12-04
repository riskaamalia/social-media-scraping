import logging
from util.UrlProcessor import UrlProcessor
from util.ConfigProcessor import ConfigProcessor


class GraphRelatedPage :

    def processor (self,dao) :
        logging.info("Processing find post : ")
        execute_process_to_db(dao)

def execute_process_to_db (dao) :
    config_proccessor = ConfigProcessor()
    token = config_proccessor.facebook_token("token")

    fb_pages = dao.get_page()

    for page in fb_pages :
        url_page = page[0]
        keyword = page[1]
        logging.info("Get content from fb page :"+url_page)
        if "/pages/" not in url_page :
            page_name = url_page.split("/")[3]
        else :
            page_name = url_page.split("/")[4]
        logging.info("Page name : "+page_name)
        graph_url = "https://graph.facebook.com/v2.10/"+page_name+"/likes?access_token="+token
        get_body = UrlProcessor().get_json_body(graph_url)
        if get_body is not None :
            json_body = get_body['data']
            total_write = 0
            for data in json_body :
                try :
                    get_id = data['id']
                    graph_get_name = "https://graph.facebook.com/v2.10/"+get_id+"?access_token="+token+"&fields=link"
                    json_get_name = UrlProcessor().get_json_body(graph_get_name)
                    if json_get_name is not None :
                        get_name = json_get_name['link']
                        if dao.is_url_page_exist(get_name) == 0 :
                            row = (get_name,keyword )
                            dao.add_page(row)
                            total_write=total_write+1
                            logging.info("Write : "+get_name+" total write : "+str(total_write))
                except Exception as e:
                    logging.info (e)
