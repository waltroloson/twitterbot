import tweepy

__author__ = 'Jacek Aleksander Gruca'


# This class provides persistence abstraction.
class TwitterApi(object):
	#
	def __init__(self, consumer_token, consumer_secret, access_token, access_token_secret):
		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)
		public_tweets = self.api.home_timeline()

		for tweet in public_tweets:
			print tweet.text

	def unfollow(self, handles_to_unfollow):
		return

	def follows_me(self, handle):
		return False

	def is_followed_by_me(self, handle):
		return True
