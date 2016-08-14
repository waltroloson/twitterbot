import argparse
import pandas

import ConfigParser

from _lib.Queue import Queue
from _lib.Handler import Handler
from _lib.TwitterApi import TwitterApi
from _lib.PersistentStore import PersistentStore

__author__ = 'Jacek Aleksander Gruca'

doc = '''
Welcome to TwitterBot. This script follows Twitter handles according to the logic specified in the README file.
'''

# argparse is used to parse command line parameters
parser = argparse.ArgumentParser(description=doc)
parser.add_argument('INPUT_FILE', action='store', help='read handles from input file')
args = parser.parse_args()

# ConfigParser parses the config file which stores user configuration
config = ConfigParser.ConfigParser()
config.read('config.ini')

batch_count = int(config.get('TwitterBot', 'handle.batch.count'))
day_count = int(config.get('TwitterBot', 'day.count'))

# reading the input CSV file into variable df
df = pandas.read_csv(args.INPUT_FILE)
# obtaining Twitter handles from df
handles = df[pandas.notnull(df.Twitter)].Twitter.values.tolist()
handles = [handle.replace("@", "").strip() for handle in handles]

# instantiating the TwitterAPI wrapper
twitter_api = TwitterApi(
	config.get('TwitterBot', 'consumer.key'),
	config.get('TwitterBot', 'consumer.secret'),
	config.get('TwitterBot', 'access.token'),
	config.get('TwitterBot', 'access.token.secret'))

# instantiating handle storage and queue connectors
mongodb_uri = config.get('TwitterBot', 'mongodb.uri')
persistent_store = PersistentStore(mongodb_uri)
queue = Queue(mongodb_uri)

# instantiating handler and executing the periodic run
handler = Handler(twitter_api, persistent_store, queue, batch_count, day_count)
handler.run(handles)
