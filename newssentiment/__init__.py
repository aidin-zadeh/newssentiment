
import os
import time
import numpy as np
import pandas as pd
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newssentiment.plot import Scatter
# get Twitter API keys
from newssentiment.conf import (consumer_key,
                                consumer_secret,
                                access_token,
                                access_token_secret)
# number of tweets per page
N_PAGE_TWEETS = 20


class TweetSentiment(object):

    def __init__(self, n_tweets=100, verbose=False):

        self.n_tweets = n_tweets
        self.verbose = verbose

        # get number of pages
        self.n_pages = np.ceil(n_tweets / N_PAGE_TWEETS).astype(int)
        # setup tweepy API authentication
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        # declare 'SentimentIntensityAnalyzer' instance
        self.analyzer = SentimentIntensityAnalyzer()

    def get_scores(self, queries):

        sentiments = []
        if not hasattr(queries, "__iter__"):
            queries = [queries]
        for query in queries:
            # append results to sentiments
            sentiments += self.get_score(query)

        # convert sentiments to DataFrame
        df = pd.DataFrame.from_dict(sentiments)
        # reorder data frame columns
        df = df[["Outlet", "Date", "Positive", "Negative", "Neutral", "Compound", "Tweets Ago"]]
        return df

    def get_score(self, query):
        sentiments = []
        oldest_tweet = None
        count = 0
        for p in range(self.n_pages):
            public_tweets = self.api.user_timeline(query, max_id=oldest_tweet)
            for index, tweet in enumerate(public_tweets):

                if self.verbose:
                    print("[{:s}] {:4}-({:3d} {:4d}) --> {:s} ".format(
                        query, count + 1, p, index, tweet["text"]
                    ))

                # get sentiments
                score = self.analyzer.polarity_scores(tweet["text"])
                compound = score["compound"]
                pos = score["pos"]
                neu = score["neu"]
                neg = score["neg"]
                tweets_ago = count

                # oet Tweet ID, subtract 1, and assign to oldest_tweet
                oldest_tweet = tweet['id'] - 1

                # append to sentiments list
                sentiments.append(
                    {"Outlet": query,
                     "Date": tweet["created_at"],
                     "Compound": compound,
                     "Positive": pos,
                     "Negative": neu,
                     "Neutral": neg,
                     "Tweets Ago": tweets_ago})
                # increment counter
                count += 1

        return sentiments


class TweetSentimentBot(TweetSentiment):

    def __init__(self, screen_name="NewsSentiment", *args, **kwargs):

        super(TweetSentiment, self).__init__(*args, **kwargs)

        self.bot_screen_name = screen_name
        self._total_tweets = 0

    def eval_mentions(self, since_id):

        mentions = self.api.mentions_timeline(since_id)
        n_mentions = len(mentions)

        if self.verbose:
            if n_mentions > 0:
                print(f"{n_mentions} mentions retrieved since last scan!")
            else:
                print(f"No mention since last scan!")

        if n_mentions > 0:

            mention_queries = []
            for mention in mentions:
                # parse mention
                mention_parsed = self.parse_mention(mention)
                ffname = self.respond_queries(mention_parsed["queries"])

        return ffname

    def parse_mention(self, mention):

        print(mention.keys())

        mention_id = mention["id"]
        mention_screen_name = mention["user"]["screen_name"]
        queries = []
        # retrieve users mentions screen names
        for elem in mention["entities"]["user_mentions"]:
            if elem["screen_name"] != self.bot_screen_name:
                queries.append(elem["screen_name"])
        return {"id": mention_id, "screen_name": mention_screen_name, "queries": queries}

    def respond_queries(self, queries):

        for query in queries:
            sentiments =  self.get_score(query)
            ffname = self.plot_sentiments(sentiments, query)
        return 0

    def plot_sentiments(self, sentiments, query=""):

        # get current time
        currtime = time.gmtime()
        currtimestr = time.strftime("%Y-%m-%d-%H-%M", currtime)

        df = pd.DataFrame(sentiments)
        df = df.reset_index()
        df.plot('index', 'compound', linestyle='-', marker='o', alpha=0.75)

        x = df.index.values
        y = df["Compound"].values
        title = f"Sentiment Analysis of {query}" + os.linesep + f"{currtimestr}"

        scatter = Scatter()
        scatter.figsize = (15, 12)
        scatter.marker = "o-"
        scatter.markersize = 12
        scatter.markeredgewidth = 1
        scatter.markerfacecolor = "blue"
        scatter.markeredgecolor = "white"
        scatter.alpha = 0.7
        scatter.xlim = [-len(x)-2, 2]
        scatter.ylim = [-1, 1]
        scatter.xlabel = "Tweets Ago"
        scatter.ylabel = "Tweet Polarity"
        scatter.title = title
        scatter.ax.spines['top'].set_visible(False)
        scatter.ax.spines['right'].set_visible(False)
        scatter.ax.spines['bottom'].set_visible(False)
        scatter.ax.spines['left'].set_visible(False)
        scatter.label = query
        scatter(x, y)

        t = time.strftime("%Y-%m-%d-%H-%M", currtime)
        ffname = os.path.join("data", "int", f"compound-scatter-{t}")
        scatter.fig.savefig(ffname, transparent=False, bbox_inches="tight")
        return ffname








