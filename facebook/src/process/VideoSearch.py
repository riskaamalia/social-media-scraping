import re
import time
import logging

from datetime import datetime

from selenium.common.exceptions import NoSuchElementException

from util.ConfigProcessor import ConfigProcessor
from util.UrlProcessor import UrlProcessor
import SendToDb

config_processor = ConfigProcessor()
loop_max = config_processor.config_loop()

def processor (driver,dao,keyword) :
    for kw in keyword :
        logging.info("Processing finds posts from queries with keyword : "+kw)
        execute_process_to_db(driver, kw.replace(" ","%20"),dao)
    driver.quit()

def execute_process_to_db (driver, keyword, dao) :
        config_proccessor = ConfigProcessor()
        token = config_proccessor.facebook_token("token",'id')

        if str(keyword).__len__() == 0 :
            keyword = "lucu"

        driver.get("https://www.facebook.com/search/videos/?q="+keyword)

        scroll_loop = 1
        first_scroll = 0
        total_write = 0
        last_scroll = driver.get_window_size()['height']

        # add this in config to be set , the total loop , and until page go to the very bottom
        while scroll_loop < loop_max :

            # find all related link from posts
            elems = driver.find_elements_by_xpath("//div[@id='browse_result_area']//a[@href]")
            try :
                for elem in elems:
                    url = elem.get_attribute("href")
                    regex = r'(https://www.facebook.com/)(.*)(/videos/)(.*)(/)$'
                    if re.match(regex,url) :
                        # insert into db
                        if dao.is_url_video_exist(url) == 0 :
                            # get total video like using API
                            video_id = url.split('/')[5]
                            video_page_name = url.split('/')[3]
                            try :
                                get_json = "https://graph.facebook.com/v2.10/"+video_id+"/likes?access_token="+token+"&summary=true&fields=total_count"
                                get_total = UrlProcessor().get_json_body(get_json)['summary']['total_count']
                            except Exception as e :
                                logging.info("get total "+e.message)
                                get_total = 0
                            row = (url,"from search",keyword,get_total,str(datetime.now().strftime('%Y-%m-%d')) )
                            dao.add_video(row)
                            total_write=total_write+1
                            logging.info(url+"Write total write : "+str(total_write))

                            try :
                                # send to others, video page
                                video_page = "https://www.facebook.com/"+video_page_name+"/"
                                logging.info("Video page name : "+video_page)
                                get_json = "https://graph.facebook.com/v2.10/"+video_page_name+"?access_token="+token+"&fields=fan_count,about"
                                get_total = UrlProcessor().get_json_body(get_json)['fan_count']
                                get_id = UrlProcessor().get_json_body(get_json)['id']

                                # get latest date video
                                video_list = "https://graph.facebook.com/v2.10/"+video_page_name+"/videos?access_token="+token+"&limit=1000"
                                video_list = UrlProcessor().get_json_body(video_list)
                                video_data = video_list['data'][0]
                                total_video = len(video_list['data'])
                                video_id = video_data['id']
                                url_time = "https://graph.facebook.com/v2.10/"+video_id+"?access_token="+token+"&fields=created_time"
                                video_time = UrlProcessor().get_json_body(url_time)['created_time']

                                try :
                                    get_about = UrlProcessor().get_json_body(get_json)['about']
                                except :
                                    get_about = ''

                                # get total video in a page
                                try :
                                    while video_list['paging']['next'].__len__ > 0 :
                                        video_list = video_list['paging']['next']
                                        video_list = UrlProcessor().get_json_body(video_list)
                                        total_video = total_video + len(video_list['data'])
                                except Exception as e:
                                    logging.info("Does not have next in video")
                                logging.info("total video "+str(total_video))

                                if dao.is_url_page_video_exist(video_page) == 0 :
                                    row=(video_page,keyword,get_total)
                                    dao.add_video_page(row)
                                dict = {'source': 'facebook', 'ref_id': str(get_id), 'url': video_page, 'title' : video_page_name, 'language' : ''
                                , 'keyword' : keyword,'latest' : str(video_time), 'like' : get_total , 'summary' : str(get_about), 'total' : total_video }
                                SendToDb.send_video(video_page, dict)
                            except Exception as e :
                                logging.info("No video")
                                logging.info(e.message)

                logging.info("Scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
                driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
                first_scroll = last_scroll * (scroll_loop - 1)

                time.sleep(3)
                scroll_loop = scroll_loop + 1

                time.sleep(5)

                try :
                    driver.find_element_by_xpath("//div[@class='_24j']")
                    logging.info("Finish Loop")
                    break
                except NoSuchElementException:
                    continue

            except Exception as e :
                logging.info(str(e.message))

