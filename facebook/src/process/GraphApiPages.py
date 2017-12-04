import logging
import SendToDb

from datetime import datetime
from util.UrlProcessor import UrlProcessor


def processor (dao,token,limit) :
    logging.info("Processing find post : ")
    execute_process_to_db(dao,token,limit)

def execute_process_to_db (dao,token,limit) :
    fb_pages = dao.get_page()
    count = 1
    for page in fb_pages :
        try :
            url_page = page[0]
            keyword = page[1]
            logging.info("Get content from fb page :"+url_page+" count : "+str(count))
            count=count+1
            if "/pages/" not in url_page :
                page_name = url_page.split("/")[3]
            else :
                page_name = url_page.split("/")[4]
            logging.info("Page name : "+page_name)
            graph_url = "https://graph.facebook.com/v2.10/"+page_name+"/posts?access_token="+token+"&fields=link&limit="+str(limit)
            get_body = UrlProcessor().get_json_body(graph_url)
            if get_body is not None :
                json_body = get_body['data']
                total_write = 0
                for data in json_body :
                    get_link = data['link']
                    if get_link.find("facebook.com") == -1:
                        # insert into db
                        url = UrlProcessor().get_article_source(get_link)
                        SendToDb.send(get_link, keyword)
                        if dao.is_url_domain_exist(url) == 0 :
                            # row = (url,get_link,url_page,keyword,str(datetime.now().strftime('%Y-%m-%d')) )
                            # dao.add_source(row)
                            total_write=total_write+1
                            logging.info("Write : "+get_link+" total write : "+str(total_write))
            logging.info("Deleted Page : "+dao.delete_page(url_page))
        except Exception as e:
            logging.info(str(e.message))




