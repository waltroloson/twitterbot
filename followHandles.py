import argparse
import pandas

import ConfigParser

from _lib.Handler import Handler
from _lib.TwitterApi import TwitterApi

__author__ = 'Jacek Aleksander Gruca'

doc = '''
Welcome to TwitterBot. This automaton follows Twitter handles according to the logic specified in the README file.
'''

parser = argparse.ArgumentParser(description=doc)
parser.add_argument('INPUT_FILE', action='store', help='read handles from input file')

args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read('config.ini')

batch_count = int(config.get('TwitterBot', 'handle.batch.count'))
day_count = int(config.get('TwitterBot', 'day.count'))

df = pandas.read_csv(args.INPUT_FILE)
handles = df[pandas.notnull(df.Twitter)].Twitter.values.tolist()

handles = [handle.replace("@", "") for handle in handles]

twitter_api = TwitterApi(
	config.get('TwitterBot', 'consumer.key'),
	config.get('TwitterBot', 'consumer.secret'),
	config.get('TwitterBot', 'access.token'),
	config.get('TwitterBot', 'access.token.secret'))

handler = Handler(twitter_api, batch_count, day_count)
handler.run(handles)
