import oauth2
import json
import logging
import database
import configuration
from time import sleep

def trending_topic (country) :
    is_next = True

    values = configuration.get_api_key(country)

    consumer_key = values[1].split(' = ')[1]
    consumer_secret = values[2].split(' = ')[1]
    token_key = values[3].split(' = ')[1]
    token_secret = values[4].split(' = ')[1]

    # indonesia woeid base on yahoo --> need for accesing twitter API trending topic
    # got from here http://woeid.rosselliot.co.nz/lookup/indonesia
    woeid = values[5].split(' = ')[1]
    base_url_trending = values[6].split(' = ')[1] + woeid

    while is_next:
        try:
            # using http rest get ` oauth authentication
            consumer = oauth2.Consumer(consumer_key, consumer_secret)
            token = oauth2.Token(token_key, token_secret)
            client = oauth2.Client(consumer, token)
            resp, content = client.request(base_url_trending, method="GET", body=b'', headers=None)

            results = json.loads(content)[0]['trends']
            date = json.loads(content)[0]['created_at']
            logging.info('trending topic on date :'+date)
            #print 'trending topic on date :'+date
            for result in results :
                trend = result['name'].replace('#','').replace(' ','%20').lower()
                #print 'keyword from trending topic : '+trend
                logging.info('keyword from trending topic : '+trend)

                # send to search and get tweets and url
                search_7_days(trend,3,country)

            #print 'sleep for update results of trending topic in 20 minutes'
            logging.info('sleep for update results of trending topic in 20 minutes')
            sleep(1200)
        except Exception as e:
            logging.exception(str(e.message))
            is_next = False

def search_7_days (keyword, thread_id,country) :
    is_next = True
    values = configuration.get_api_key(country)

    base_url = values[0].split(' = ')[1]
    consumer_key = values[1].split(' = ')[1]
    consumer_secret = values[2].split(' = ')[1]
    token_key = values[3].split(' = ')[1]
    token_secret = values[4].split(' = ')[1]

    # params = '?q=' + keyword + '&lang=id&include_entities=true&count=100'
    params = '?q=' + keyword + '&include_entities=true&count=100'
    while is_next :
        try :
            url = base_url + params
            # using http rest get with oauth authentication

            consumer = oauth2.Consumer(consumer_key, consumer_secret)
            token = oauth2.Token(token_key, token_secret)

            client = oauth2.Client(consumer, token)
            resp, content = client.request(url, method="GET", body=b'', headers=None)

            results = json.loads(content)

            try :
                tweets = results['statuses']
                for tweet in tweets :
                    try :
                        if len(tweet['entities']['urls']) > 0 :
                            url = tweet['entities']['urls'][0]['expanded_url']
                            if 'twitter.com' not in url :
                                # logging.info( 'tweet : '+ tweet['text'].strip())
                                #print 'tweet : '+ tweet['text'].strip()
                                logging.info( 'url : '+url)
                                #print 'url : '+url
                                database.send(url, keyword)
                                # logging.info( '=========================================')
                                #print '========================================='
                    except Exception as e :
                        logging.info(str(e.message))

                if thread_id == 1:
                    next = 'next_results'
                else :
                    next = 'refresh_url'

                if len(results['search_metadata'][next]) < 1 or next is 'refresh_url':
                    is_next = False
                else :
                    logging.info( 'go to next result')
                    #print 'go to next result'
                    params = results['search_metadata'][next]

                # in order to avoid limit
                logging.info('in order to avoid limit sleep for a while ....')
                # print 'in order to avoid limit sleep for a while ....'
                sleep(60)
            except Exception as e :
                logging.exception(str(e.message))

                # in order to avoid limit
                logging.exception('in order to avoid limit sleep in 10 minutes ....')
                #print 'in order to avoid limit sleep for a while ....'
                sleep(600)

        except Exception as e :
            logging.exception(str(e.message))
            #print str(e.message)
            is_next = False


