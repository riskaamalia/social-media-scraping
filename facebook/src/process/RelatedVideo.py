import logging
import re
import SendToDb

from time import sleep
from util.ConfigProcessor import ConfigProcessor
from util.UrlProcessor import UrlProcessor

class RelatedVideo :
    def processor (self,driver,dao) :
        logging.info("Processing find video from related video : ")
        execute_process_to_db(driver,dao)

def execute_process_to_db (driver,dao) :
    config_proccessor = ConfigProcessor()
    token = config_proccessor.facebook_token("token",'id')
    fb_pages = dao.get_video()
    total_write = 0

    for page in fb_pages :
        url_video = page[0]
        sleep(10)
        logging.info("Get video url :"+url_video)
        driver.get(url_video)

        sleep(2)
        try :
            elems = driver.find_elements_by_xpath("//a[@class='_u2s']")
        except Exception as e:
            logging.info(str(e.message))
            elems = []

        for elem in elems:
            try :
                url_page = elem.get_attribute("href")
                url_page = 'https://www.facebook.com/' + url_page.split('/')[3] + '/'
                logging.info("get this video : " + url_page)
                is_exist = dao.is_url_page_video_exist(url_page)
                if is_exist == 0:
                    if "/pages/" not in url_page:
                        page_name = url_page.split("/")[3]
                    else:
                        page_name = url_page.split("/")[4]
                    logging.info("Page name : " + page_name)
                    try:
                        get_json = "https://graph.facebook.com/v2.10/" + page_name + "?access_token=" + token + "&fields=fan_count,about"
                        json = UrlProcessor().get_json_body(get_json)
                        get_total = json['fan_count']
                        get_id = json['id']
                        row = (url_page, "related video", get_total)
                        dao.add_video_page(row)
                    except Exception as e:
                        get_total = 0
                        row = (url_page, "related video", get_total)
                        dao.add_video_page(row)

                    # get latest date video
                    video_list = "https://graph.facebook.com/v2.10/" + page_name + "/videos?access_token=" + token + "&limit=1000"
                    video_list = UrlProcessor().get_json_body(video_list)
                    if len(video_list['data']) > 0:
                        video_data = video_list['data'][0]
                        total_video = len(video_list['data'])
                        video_id = video_data['id']
                        url_time = "https://graph.facebook.com/v2.10/" + video_id + "?access_token=" + token + "&fields=created_time"
                        video_time = UrlProcessor().get_json_body(url_time)['created_time']
                        logging.info("Video ID " + video_id)
                        try:
                            get_about = UrlProcessor().get_json_body(get_json)['about']
                        except:
                            get_about = ''

                        dict = {'source': 'facebook', 'ref_id': str(get_id), 'url': str(url_page), 'title': str(page_name),
                                'language': '', 'keyword': 'related video', 'latest': str(video_time), 'like': get_total,
                                'summary': str(get_about), 'total': total_video}
                        SendToDb.send_video(url_page, dict)
                        row = (url_page, page[2], 0)
                        dao.add_video_page(row)
                        total_write = total_write + 1
                        logging.info("Write : " + url_page + " total write : " + str(total_write))
            except Exception as e :
                logging.info(str(e.message))