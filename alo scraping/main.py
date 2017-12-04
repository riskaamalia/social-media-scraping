from BeautifulSoup import BeautifulSoup
from datetime import datetime
import urllib2
import database
import logging
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils

common_utils.setup_logging('alodokter.log')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def get_xml_topic () :
    xml_url = []

    req = urllib2.Request('http://www.alodokter.com/sitemap.xml', headers=hdr)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)

    xmls = soup.findAll('loc')
    for xml in xmls :
        url = str(xml).replace('</loc>','').replace('<loc>','')
        if 'topic' in url and '2017' in url :
            xml_url.append(url)

    return xml_url

def execute () :
    results = get_xml_topic()
    for result in results :
        try :
            # print 'xml url topic : '+result
            logging.info('xml url topic : '+result)

            req = urllib2.Request(result, headers=hdr)
            page = urllib2.urlopen(req).read()

            soup = BeautifulSoup(page)
            xmls = soup.findAll('loc')
            for xml in xmls :
                try :
                    question_url = str(xml).replace('</loc>','').replace('<loc>','')
                    # print 'scrape this site : '+question_url
                    # logging.info('scrape this site : '+question_url)
                    scrape_question(question_url, hdr)

                    # sleep(5)
                    # logging.info('sleep for a while ... ')
                    # print 'sleep for a while ... '
                except Exception as e :
                    logging.info(str(e.message))

            # logging.info('change xml topic ...')
        except Exception as e :
            logging.exception(str(e.message))


def scrape_question (question_url, hdr) :
    '''
    CREATE TABLE `alodokter_questions` (
    `metadata_id` int(11) NOT NULL AUTO_INCREMENT,
    `metadata_source` varchar(200) DEFAULT NULL,
    `metadata_url` varchar(350) DEFAULT NULL,
    `metadata_title` varchar(350) DEFAULT NULL,
    `metadata_article_tag` varchar(200) DEFAULT NULL,
    `questioner_image` varchar(300) DEFAULT NULL,
    `questioner_name` varchar(300) DEFAULT NULL,
    `questioner_profile_link` varchar(300) DEFAULT NULL,
    `questioner_question` text DEFAULT NULL,
    `questioner_date` datetime DEFAULT NULL,
    `expert_image` varchar(300) DEFAULT NULL,
    `expert_name` varchar(300) DEFAULT NULL,
    `expert_profile_link` varchar(300) DEFAULT NULL,
    `expert_answer` text DEFAULT NULL,
    `expert_date` datetime DEFAULT NULL,
    PRIMARY KEY (metadata_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

    article_tag = ''
    questioner_image = ''
    questioner_name = ''
    questioner_profile_link = ''
    questioner_question = ''
    questioner_date = ''
    expert_image = ''
    expert_name = ''
    expert_profile_link = ''
    expert_answer = ''
    expert_date = ''

    try :
        # insert result into database
        if str(database.get_url(question_url)) == '()' :
            req = urllib2.Request(question_url, headers=hdr)
            page = urllib2.urlopen(req).read()
            soup = BeautifulSoup(page)

            get_title = soup.find("h1", {"class": "highlight-title-small"})
            title = str(get_title.contents[0]).strip()

            # print 'title : '+title
            # logging.info('title : ' + title)

            # get article tag
            try:
                decline_tag = ['alodokter', 'kesehatan', 'medis', 'penyakit', 'komunitas kesehatan', 'dokter',
                               'konsultasi kesehatan', 'informasi kesehatan']
                get_article_tag = soup.findAll("meta", property="article:tag")
                # only get one example tag
                for meta in get_article_tag:
                    is_article_tag_exist = True
                    for decline in decline_tag:
                        if decline in str(meta):
                            is_article_tag_exist = False

                    if is_article_tag_exist:
                        article_tag = str(meta).split('content="')[1].replace('" />', '').strip()

                # print 'article tag : '+article_tag
                # logging.info('article tag : ' + article_tag)
            except:
                article_tag = ''

            div_question_and_answer = soup.findAll("div", {"class": "alodokter-komunitas-topik"})
            loop = 0
            logging.info('total div : ' + str(div_question_and_answer.__len__()))
            for div in div_question_and_answer:
                is_from_doctor = True
                div_id = str(div.get('id'))

                # image
                try:
                    get_image = div("img", {"class": "avatar avatar-fb"})
                    image = str(get_image).split('"')[1].strip()

                    # print image
                    # logging.info('image : ' + image)
                except:
                    image = ''

                # name and profile link
                try:
                    get_users = div("a", {"class": "bbp-author-name"})
                    user_name = str(get_users).split('>')[1].replace(' </a', '').replace('</a', '').strip()
                    profile_link = 'alodokter.com' + str(get_users).split('"')[1].strip()

                    # print user_name
                    # print profile_link
                    # logging.info('name : ' + user_name)
                    # logging.info('profile link : ' + profile_link)
                except:
                    user_name = ''
                    profile_link = ''

                # question or answer
                try:
                    get_text = div("div", {'class': 'alodokter-bbp-content-' + div_id})

                    contents = get_text[0].contents
                    text = ''
                    for content in contents :
                        text = text + str(content).replace('"', '\\"').replace("'","\\'").strip()

                    # detect not question from doctor
                    if len(text) < 500 and '<p>' not in text and loop > 0 and 'dr.' not in text:
                        if 'alodokter.com' not in text or 'dr.' not in text:
                            text = ''
                            user_name = ''
                            profile_link = ''
                            is_from_doctor = False


                except:
                    text = ''

                # date
                try:
                    get_date = div("p", {"class": "bbp-reply-post-date-right"})
                    ori_date = str(get_date).split('>')[1].replace('</p', '')
                    original_format = '%b %d, %Y at %I:%M %p'
                    format = '%Y-%m-%d %H:%M'
                    get_ori_date = datetime.strptime(ori_date, original_format)
                    text_date = get_ori_date.strftime(format)

                    # print 'date : '+text_date
                    # logging.info('date : ' + text_date)
                except:
                    text_date = ''

                if loop == 0:
                    questioner_image = image
                    questioner_name = user_name
                    questioner_profile_link = profile_link
                    questioner_question = text
                    questioner_date = text_date
                    logging.info('text : ' + text[0:100] + '.....')
                elif len(questioner_question) > 5 and is_from_doctor == True :
                    expert_image = image
                    expert_name = user_name
                    expert_profile_link = profile_link
                    expert_answer = text
                    expert_date = text_date
                    logging.info('text : ' + text[0:100] + '.....')
                    break

                loop = loop + 1

            logging.info('# insert into db with url : ' + question_url)
            database.insert(question_url, title, article_tag, questioner_image, questioner_name,
                            questioner_profile_link,
                            questioner_question, questioner_date, expert_image, expert_name, expert_profile_link,
                            expert_answer, expert_date)
        # else:
            # logging.info('# already exist : ' + question_url)

    except Exception as e :
        # print str(e.message)
        logging.exception(str(e.message))


execute()
