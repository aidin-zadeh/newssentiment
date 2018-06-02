import os, sys, inspect
import time
from newssentiment import TweetSentiment 

# add parent dir to system dir
currdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
rootdir = os.path.dirname(currdir)
# sys.path.insert(0, rootdir)