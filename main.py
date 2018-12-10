import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from threading import Thread
import json
from textblob import TextBlob
import pandas as pd
from sklearn.externals import joblib
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options

used_features = ['screen_name_binary', 'name_binary', 'description_binary', 'status_binary', 'listed_count_binary',
                 'verified', 'followers_count', 'friends_count', 'statuses_count']
bag_of_words_bot = 'bot', 'b0t'

define("port", default=8888, type=int)

websockets = []


class IndexHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self, *args):
        print("New connection")
        websockets.append(self)
        self.write_message("Welcome!")

    def on_message(self, message):
        print("New message {}".format(message))
        self.write_message(message.upper())

    def on_close(self):
        websockets.remove(self)
        print("Connection closed")


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebSocketHandler),
])


def contains(str):
    for word in bag_of_words_bot:
        if word in str.lower():
            return True
    return False


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
            print("Bot: " + str(result[0]))
            print("Sentiment: " + str(get_sentiment(twitt["text"])))
            print()
            for socket in websockets:
                socket.write_message(twitt)
            return True
        except Exception as e:
            print(e)

    def on_error(self, status):
        print(status)
        return True


def listen(tags=['#android', "#java", "#kotlin", "#spring", ""]):
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=tags)


def get_sentiment(text):
    textblob = TextBlob(text)
    if textblob.detect_language() != 'en':
        textblob = textblob.translate(to="en")
    return textblob.sentiment


if __name__ == '__main__':
    consumer_key = 'sLV09OPi3alMMLRk0HRiCu0E7'  # os.environ['CONSUMER_KEY']
    consumer_secret = 'iKesLG8B91nZLJ84Nc46TeLfhcppV9lDhF5yRFiVg1VNY9elJz'  # os.environ['CONSUMER_SECRET']
    access_token = '3317470103-A5IdrYg3u8cgAmbvvm8asO6JV2vs8UgXBpz0nP8'  # os.environ['ACCESS_TOKEN']
    access_secret = '6Np0ssKOPj903OPG3XZriGCFdgKAT93UWNU1YLuNVqykg'  # os.environ['ACCESS_SECRET']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    final_model = joblib.load("model.sav")

    thread = Thread(target=listen)
    thread.start()

    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
