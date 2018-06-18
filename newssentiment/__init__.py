
import os, sys, inspect
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newssentiment.plot import Trend
# get Twitter API keys
from newssentiment.conf import (consumer_key,
                                consumer_secret,
                                access_token,
                                access_token_secret)

# get current dir
currdir = os.path.dirname(os.path.abspath(inspect.getabsfile(inspect.currentframe())))
rootdir = os.path.dirname(currdir)

plt.ioff()
plt.style.use('seaborn')

# number of tweets per page
N_PAGE_TWEETS = 20


class TweetSentiments(object):

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

                if self.verbose == 1:
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


class TweetSentimentsBot(TweetSentiments):

    def __init__(self, screen_name="NewsSentiment", *args, **kwargs):

        super(TweetSentimentsBot, self).__init__(*args, **kwargs)

        self.bot_screen_name = screen_name
        self._since_id = 1
        self._total_tweets = 0

    def eval_mentions(self, since_id=None):

        if since_id:
            self._since_id = since_id

        try:
            if self.verbose == 2:
                print("Scanning for mentions...", end="")
            mentions = self.api.mentions_timeline(self._since_id)[::-1]
            if self.verbose == 2:
                print("completed.", end="")
        except tweepy.TweepError as e:
            print("Error: {:s}".format(str(e)))
        n_mentions = len(mentions)

        if self.verbose == 2:
            if n_mentions > 0:
                print(f" {n_mentions} mentions retrieved since the last scan!")
            else:
                print(f" No mention since the last scan!")

        if n_mentions > 0:

            # list to store unique user screen names
            mention_users_processed = []
            for mention in mentions:
                # parse mention
                mention_parsed = self.parse_mention(mention)
                if mention_parsed["screen_name"] not in mention_users_processed and \
                        len(mention_parsed["queries"]) != 0:
                    self._since_id = mention_parsed["id"]
                    self.respond_queries(mention_parsed["screen_name"], mention_parsed["queries"])

                    mention_users_processed.append(mention_parsed["screen_name"])
                elif mention_parsed["screen_name"] in mention_users_processed:
                    print("Queries from {:s}...skipped. Multiple mentions!".format(mention_parsed["screen_name"]))
                elif n_mentions == 0:
                    print("Queries from {:s}...skipped. Invalid queries!".format(mention_parsed["screen_name"]))

            return mention_parsed["id"]
        else:
            return self._since_id

    def parse_mention(self, mention):

        mention_id = mention["id"]
        mention_screen_name = mention["user"]["screen_name"]
        queries = []
        # retrieve users mentions screen names
        for elem in mention["entities"]["user_mentions"]:
            if elem["screen_name"] != self.bot_screen_name:
                queries.append(elem["screen_name"])

        return {"id": mention_id, "screen_name": mention_screen_name, "queries": queries}

    def respond_queries(self, screen_name, queries):
        # list to store store unique queries
        queries_processed = []
        for query in queries:
            if self.verbose == 2:
                print(f"Responding to {screen_name} for {query}...", end="")
            if query not in queries_processed:
                try:
                    sentiments = self.get_score(query)
                    ffname = self.plot_sentiments(sentiments, query)
                except:
                    pass
                try:
                    queries_processed.append(query)
                    self.api.update_with_media(ffname, "@{:s}".format(screen_name))
                    if self.verbose == 2:
                        print("completed.")
                except tweepy.TweepError as e:
                    print("Error: {:s}".format(str(e)))
            else:
                if self.verbose == 2:
                    print("skipped. (duplicate query)")

    def plot_sentiments(self, sentiments, query=""):

        # get current time
        currtime = time.gmtime()
        currtimestr = time.strftime("%Y-%m-%d-%H-%M", currtime)

        df = pd.DataFrame(sentiments)
        df = df.reset_index()

        x = df.index.values
        y = df["Compound"].values
        title = f"Sentiment Analysis of {query}" + os.linesep + f"{currtimestr}"

        trend = Trend()
        trend.figsize = (8, 5)
        trend.color = "blue"
        trend.marker = "o"
        trend.linestyle = "-"
        trend.markersize = 12
        trend.markeredgewidth = 1
        trend.markerfacecolor = "blue"
        trend.markeredgecolor = "white"
        trend.alpha = 0.8
        # trend.xlim = [-len(x)-2, 2]
        trend.ylim = [-1., 1.]
        trend.xlabel = "Tweets Ago"
        trend.ylabel = "Tweet Polarity"
        trend.title = title
        trend.ax.spines['top'].set_visible(False)
        trend.ax.spines['right'].set_visible(False)
        trend.ax.spines['bottom'].set_visible(False)
        trend.ax.spines['left'].set_visible(False)
        trend.label = query
        trend(x, y, "o-")

        t = time.strftime("%Y-%m-%d-%H-%M", currtime)
        ffname = os.path.join(currdir, "data", "int", f"compound-scatter.png")
        trend.fig.savefig(ffname, transparent=False, bbox_inches="tight")

        return ffname


# sentiment_bot = TweetSentimentsBot(verbose=True)
# dd = sentiment_bot.eval_mentions()
# mentions = sentiment_bot.api.mentions_timeline(since_id=2)


