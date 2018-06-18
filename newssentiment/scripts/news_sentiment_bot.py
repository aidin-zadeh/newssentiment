
import time
import argparse
import numpy as np
from newssentiment import TweetSentimentsBot
from tqdm import tqdm


argparser = argparse.ArgumentParser(
    description="Execute a twitter bot that performs sentiment analysis for user-names as specified in mentions.",
    epilog="Example of use: `python -m newssentiment.scripts.news_sentiment_bot --tweets 500 --wait 1 --verbose 2`"
)

argparser.add_argument(
    "-t",
    "--tweets",
    default=10,
    type=int,
    help="Number of recent tweets to perform sentiment analysis on. (default = 500)",
)
argparser.add_argument(
    "-w",
    "--wait",
    default=5,
    type=int,
    help="Minutes to wait before re-scaning for new mentions. "
         "One mention per user is processed in each scan. (default = 5)",
)
argparser.add_argument(
    "-v",
    "--verbose",
    default=2,
    type=int,
    help="Increase output verbosity. 0: Silent. 1: print out mentions+queries, "
         "2: print out progress lines. (default = 2)",
)


def _main(args):

    n_tweets = args.tweets
    wait_time_min = args.wait
    verbose = args.verbose

    # init. an instance from TweetSentimentBot
    sentiment_bot = TweetSentimentsBot(n_tweets=n_tweets, verbose=verbose)
    # set waite time between each scan
    wait_time_sec = int(np.ceil(wait_time_min * 60))

    r_bar = " [{elapsed} < {remaining}]"
    l_bar = "Time to next scan: "
    bar_format = f"{l_bar}{r_bar}"
    # initialize since_id
    since_id = 1
    is_run = True
    cnt = 0
    while is_run:
        since_id = sentiment_bot.eval_mentions(since_id=since_id)
        cnt += 1
        for i in tqdm(range(wait_time_sec), desc="Time to next scan: ", bar_format=bar_format):
            time.sleep(1)


if __name__ == "__main__":
    args = argparser.parse_args()
    _main(args)




