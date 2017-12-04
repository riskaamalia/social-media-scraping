import logging
from util.UrlProcessor import UrlProcessor
from time import sleep
import SendToDb

def processor (dao,keyword,token,limit) :
    for kw in keyword :
        try :
            logging.info("Processing finds pages for video from queries with keyword : "+kw)
            execute_process_to_db(kw.replace(" ","%20"),dao,token,limit)
        except Exception as e :
            logging.exception(str(e.message))
        logging.info('sleep for a while in 300 seconds')
        sleep(300)
    logging.info('sleep in 10 minutes for regenerate page ....')
    sleep(600)


def execute_process_to_db (keyword, dao, token, limit) :

    base_url = "https://graph.facebook.com/v2.10/search?access_token="+token+"&fields=link&type=page&limit="+str(limit)+"&q="

    url = base_url+keyword
    get_body = UrlProcessor().get_json_body(url)
    json_body = get_body['data']
    total_write = 0
    for data in json_body :
        try :
            # insert into db
            total_write=total_write + 1
            # logging.info(keyword+" URL Page : "+data['link'])
            if dao.is_url_page_video_exist(data['link']) == 0 :
                if "/pages/" not in data['link'] :
                    page_name = data['link'].split("/")[3]
                else :
                    page_name = data['link'].split("/")[4]
                logging.info("Page name : "+page_name)
                try :
                    get_json = "https://graph.facebook.com/v2.10/"+page_name+"?access_token="+token+"&fields=fan_count,about"
                    json = UrlProcessor().get_json_body(get_json)
                    get_total = json['fan_count']
                    get_id = json['id']
                    row=(data['link'],keyword,get_total)
                    dao.add_video_page(row)
                except Exception as e :
                    get_total = 0
                    row=(data['link'],keyword,get_total)
                    dao.add_video_page(row)

                if json is not None :

                    # get latest date video
                    video_list = "https://graph.facebook.com/v2.10/"+page_name+"/videos?access_token="+token+"&limit=1000"
                    video_list = UrlProcessor().get_json_body(video_list)
                    if len(video_list['data']) > 0 :
                        video_data = video_list['data'][0]
                        total_video = len(video_list['data'])
                        video_id = video_data['id']
                        url_time = "https://graph.facebook.com/v2.10/"+video_id+"?access_token="+token+"&fields=created_time"
                        video_time = UrlProcessor().get_json_body(url_time)['created_time']
                        logging.info("Video ID "+video_id)
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

                        dict = {'source': 'facebook', 'ref_id': str(get_id), 'url': str(data['link']), 'title' : str(page_name), 'language' : '', 'keyword' : keyword,'latest' : str(video_time), 'like' : get_total , 'summary' : str(get_about), 'total' : total_video }
                        SendToDb.send_video(data['link'], dict)
                        total_write=total_write+1
                        logging.info("Write : "+data['link']+" total write : "+str(total_write))
        except Exception as e:
            logging.info(str(e.message))
