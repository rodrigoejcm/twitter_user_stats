import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time

from statistics import mean,median




path_to_chromedriver = "driver/chromedriver" 
option = webdriver.ChromeOptions()
#option.add_argument("--headless")
#option.add_argument("--incognito")
#option.add_argument('--proxy-server=46.102.106.37:13228')


browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=option)
#browser = webdriver.Chrome(executable_path = path_to_chromedriver)


path = 'json/'
url_base = 'https://twitter.com/'
url_complement = "/status/"
#jairbolsonaro/status/10567139396298096650


def find_replies_count_for_post(url_base,username, url_complement, post_id, browser):
    
    url = url_base + username + url_complement + str(post_id)
    
    browser.get(url)
    
    #selector = "div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.stream-item-footer > div.ProfileTweet-actionList.js-actions > div.ProfileTweet-action.ProfileTweet-action--reply > button > span[data-tweet-stat-count]"
    selector = "div.ProfileTweet-action.ProfileTweet-action--reply > button > span[data-tweet-stat-count]"
                
    try:
        element = WebDriverWait(browser, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
         )
        

        #span = BeautifulSoup(element.get_attribute('innerHTML').page_source, "html.parser")
        #count = span[0]['data-tweet-stat-count']
        print("-- Achou atributo")
        count = element.get_attribute("data-tweet-stat-count")
        print(count)
    
    
    except TimeoutException as error:

        try :
            element = browser.find_elements(By.CSS_SELECTOR, '#permalink-overlay-dialog > div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.stream-item-footer > div.ProfileTweet-actionList.js-actions > div.ProfileTweet-action.ProfileTweet-action--reply > button > span > span.ProfileTweet-actionCountForPresentation')
            print("-- Dentro do seg Try")
            if element:
                print("-- Dentro do if")
                print(element[0].get_attribute('outerHTML'))
                count = element[0].get_attribute('innerHTML')
                if count == None:
                    #time.sleep(100)
                    count = 0
            else:
                print("-- Dentro do else")
                count = 0
                for elm in element:
                    print(elm.get_attribute('outerHTML'))
        except NoSuchElementException as error:
            print("-- Dentro do exc ele")
            count = 0
            print("---- sem elemento "+error)

    
    
    print(count)
    return int(count)


data = {}

for root, dirs, files in os.walk(path):
    
    ### PARA CADA USUARIO
    for filename in files:
    
        with open(path + filename) as json_data:
            u_timeline = json.load(json_data)

        username = u_timeline[0]['user']['screen_name']

        data_temp = {}
        data_temp['id'] = u_timeline[0]['user']['id']

        #check to see if file is already proccessed
        if not os.path.isfile("result_json/"+str(data_temp['id'])+"_results.csv"):

            data_temp['name'] = u_timeline[0]['user']['name']
            data_temp['total_followers'] = u_timeline[0]['user']['followers_count']
            data_temp['total_posts'] = u_timeline[0]['user']['statuses_count']
            data_temp['total_following'] = u_timeline[0]['user']['friends_count']

            likes = []
            retweets = []
            replies = []

            for post in u_timeline:

                post_id = post['id']

                r_count = find_replies_count_for_post(url_base,username, url_complement, post_id, browser)
                #if r_count == 0:
                #    continue
                #else:
                likes.append(post['favorite_count'])
                retweets.append(post['retweet_count'])
                replies.append(r_count) 
            
            data_temp['total_likes'] = likes
            data_temp['total_likes_mean'] = mean(likes)
            data_temp['total_likes_median'] = median(likes)

            data_temp['total_retweets'] = retweets
            data_temp['total_retweets_mean'] = mean(retweets)
            data_temp['total_retweets_median'] = median(retweets)

            data_temp['total_replies'] = replies
            data_temp['total_replies_mean'] = mean(replies)
            data_temp['total_replies_median'] = median(replies)

            data_temp['posts_count'] = len(replies)

            data['username'] = data_temp

            result = pd.DataFrame.from_dict(data, orient='index')
            result.to_csv("result_json/"+str(data_temp['id'])+"_results.csv", sep='\t')
            
    
#result = pd.DataFrame.from_dict(data, orient='index')
#result.to_csv("results.csv", sep='\t')
    

