import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from threading import Thread
import json

import pandas as pd
import numpy as np
from sklearn.externals import joblib

used_features = ['screen_name_binary', 'name_binary', 'description_binary', 'status_binary', 'listed_count_binary',
                 'verified', 'followers_count', 'friends_count', 'statuses_count']
bag_of_words_bot = 'bot', 'b0t'


def contains(str):
    for word in bag_of_words_bot:
        if word in str.lower():
            return True
    return False


if __name__ == '__main__':
    consumer_key = 'sLV09OPi3alMMLRk0HRiCu0E7'
    consumer_secret = 'iKesLG8B91nZLJ84Nc46TeLfhcppV9lDhF5yRFiVg1VNY9elJz'
    access_token = '3317470103-A5IdrYg3u8cgAmbvvm8asO6JV2vs8UgXBpz0nP8'
    access_secret = '6Np0ssKOPj903OPG3XZriGCFdgKAT93UWNU1YLuNVqykg'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    final_model = joblib.load("model.sav")


    class MyListener(StreamListener):
        def on_data(self, data):
            try:
                twitt = json.loads(data)
                print("Message " + twitt["text"])
                user = twitt["user"]
                print("Username " + user["name"])
                data = [contains(user["screen_name"]),
                                           contains(user["name"]),
                                           contains(user["description"]),
                                           (user["statuses_count"] > 0),
                                           (user["listed_count"] < 20000),
                                           user["verified"],
                                           user["followers_count"],
                                           user["friends_count"],
                                           user["statuses_count"]]
                input_data = pd.DataFrame([data])
                result = final_model.predict(input_data)
                print("Bot :" + str(result[0]))
                return True
            except Exception as e:
                print(e)

        def on_error(self, status):
            print(status)
            return True


    def listen(tags=['#android', "#java", "#kotlin", "#spring",""]):
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=tags)


    thread = Thread(target=listen)
    thread.start()
