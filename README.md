# News Sentiment Analysis 

By *Aidin Hassanzadeh*
___

This repository contains Python/NootebookIPython files for the 'News Sentiment Analysis' project. The current implementation of this project implements the following objectives: 
- Develop a data driven approach to compare the volume of positive and negative news as tweeted by 5 major news outlets, namely CBS. CNN, BBC, Fox News and New York Times.
To this end to
- Develop a Twitter bot ([here](https://twitter.com/NewsSentiment/with_replies)) that performs sentiment analysis for other twitter accounts that mention the bot in their tweets.
Even this project was particularly implemented for sentiment analysis of news outlets, the codes can easily applied to any other Twitter accounts.
## Data
The data utilized for the fist part of this work was obtained by Twitter API on 06.14.2018 17:10 (UTC). The sentiments of tweets were estimated by [VADER-Sentiment-Analysis](https://github.com/cjhutto/vaderSentiment). 

## Report
The visual report containing the discovered insights and the detailed implementation are available by a Jupyter Noebook [here](https://github.com/aidinhass/newssentiment/blob/master/notebooks/README.md).

## Requirements
- python=3.6.5
- jupyter=1.0.0
- nb_conda=2.2.1
- numpy=1.14.2
- matplotlib=2.2.2
- pandas=0.22.0
- scipy=1.1.0
- tqdm=4.23.4
- vaderSentiment

## Directory Structure

```
.
├── docs                <- Documents related to this project.    
├── images              <- Images for README.md files.
├── newssentiment       <- source files used in this project.
│   ├── conf
│   ├── data
│   │   ├── ext
│   │   ├── int
│   │   └── raw
│   ├── images
│   ├── plot
│   └── scripts
├── notebooks           <- Ipythoon Notebook files
├── reports             <- Generated analysis as HTML, PDF, Latex, etc.
│   ├── figures         <- Generated graphics and figures used in reporting.
│   └── logs            <- Generated log files.
└── scripts             <- Scripts used in this project.

```

### Installation
Install python dependencies from  `requirements.txt` using conda.
```bash
conda install --yes --file requirements.txt
```

Or create a new conda environment `<new-env-name>` by importing a copy of a working conda environment stored at root directory :`weatherpy.yml`.
```bash
conda env create --name <new-env-name> -f "newssentimentpy.yml"
```
### Usage
#### 1. Set up authentication
The authentication keys for Twitter API are read from `newssentiment/conf/__init__.py`. Log in to your Twitter account and create a new app at [Twitter Application Management](https://apps.twitter.com/). Collect Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret and Owner Id and store at `newssentiment/conf/__init__.py`
#### 2. Run the bot
The runner script is at `newssentiment/scripts/news_sentiment_bot.py`.
```bash
python -m newssentiment.scripts.news_sentiment_bot --help
usage: news_sentiment_bot.py [-h] [-t TWEETS] [-w WAIT] [-v VERBOSE]

Execute a twitter bot that performs sentiment analysis for user-names as
specified in mentions.

optional arguments:
  -h, --help            show this help message and exit
  -t TWEETS, --tweets TWEETS
                        Number of recent tweets to perform sentiment analysis
                        on. (default = 500)
  -w WAIT, --wait WAIT  Minutes to wait before re-scaning for new mentions.
                        One mention per user is processed in each scan.
                        (default = 5)
  -v VERBOSE, --verbose VERBOSE
                        Increase output verbosity. 0: Silent. 1: print out
                        mentions+queries, 2: print out progress lines.
                        (default = 2)

Example of use: `python -m newssentiment.scripts.news_sentiment_bot --tweets
500 --wait 1 --verbose 2`
```

## References
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

## To Do
- [x] Test News Sentiment tweeter bot
- [ ] Deploy on heroku

## License
NA
