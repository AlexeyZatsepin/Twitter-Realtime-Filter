import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from threading import Thread
import json

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings

if __name__ == '__main__':
    consumer_key = 'sLV09OPi3alMMLRk0HRiCu0E7'
    consumer_secret = 'iKesLG8B91nZLJ84Nc46TeLfhcppV9lDhF5yRFiVg1VNY9elJz'
    access_token = '3317470103-A5IdrYg3u8cgAmbvvm8asO6JV2vs8UgXBpz0nP8'
    access_secret = '6Np0ssKOPj903OPG3XZriGCFdgKAT93UWNU1YLuNVqykg'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)


    class MyListener(StreamListener):
        def on_data(self, data):
            twitt = json.loads(data)
            print(twitt["user"])
            # {'id': 1066252633269256192,
            # 'id_str': '1066252633269256192',
            # 'name': 'Mobile Apps & Games',
            # 'screen_name': 'KaracaMobile',
            # 'location': None,
            # 'url': 'https://play.google.com/store/apps/developer?id=Karaca',
            # 'description': None,
            # 'translator_type': 'none', pop
            # 'protected': False, pop
            # 'verified': False, '
            # followers_count': 247,
            # 'friends_count': 1318,
            # 'listed_count': 1,
            # 'favourites_count': 193,
            # 'statuses_count': 74,
            # 'created_at': 'Sat Nov 24 08:50:12 +0000 2018',
            # 'utc_offset': None, pop
            # 'time_zone': None, pop
            # 'geo_enabled': False, pop
            # 'lang': 'en',
            # 'contributors_enabled': False, pop
            # 'is_translator': False, pop
            # 'profile_background_color': 'F5F8FA',
            # 'profile_background_image_url': '',
            # 'profile_background_image_url_https': '',
            # 'profile_background_tile': False,
            # 'profile_link_color': '1DA1F2',
            # 'profile_sidebar_border_color': 'C0DEED',
            # 'profile_sidebar_fill_color': 'DDEEF6',
            # 'profile_text_color': '333333',
            # 'profile_use_background_image': True,
            # 'profile_image_url': 'http://pbs.twimg.com/profile_images/1066253374948065280/omYTK152_normal.jpg',
            # 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1066253374948065280/omYTK152_normal.jpg',
            # 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/1066252633269256192/1543049627',
            # 'default_profile': True,
            # 'default_profile_image': False,
            # 'following': None, pop
            # 'follow_request_sent': None, pop
            # 'notifications': None} pop
            return True

        def on_error(self, status):
            print(status)
            return True


    def listen(tags=['#android', "#java", "#kotlin", "#spring"]):
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=tags)


    thread = Thread(target=listen)
    thread.start()
