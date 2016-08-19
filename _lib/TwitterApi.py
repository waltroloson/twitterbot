import tweepy

__author__ = 'Jacek Aleksander Gruca'


# This class is a TwitterAPI wrapper providing basic operations used by TwitterBot. It uses tweepy to
# interact with TwitterAPI.
class TwitterApi(object):
	#
	def __init__(self, consumer_token, consumer_secret, access_token, access_token_secret):
		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=False)
		self.my_screen_name = str(self.api.me().screen_name)

	def follow(self, handles_to_follow):
		for handle_to_follow in handles_to_follow:
			print 'Following ' + handle_to_follow + '.'
			if not self.api.create_friendship(handle_to_follow):
				return False
		return True

	def requested_to_follow(self, handle):
		print 'Checking if already requested to follow handle %s.' % handle
		return self.api.get_user(handle).follow_request_sent

	def unfollow(self, handles_to_unfollow):
		for handle_to_unfollow in handles_to_unfollow:
			print 'Unfollowing ' + handle_to_unfollow + '.'
			if not self.api.destroy_friendship(handle_to_unfollow):
				return False
		return True

	def get_my_followers(self):
		return self.api.followers(self.my_screen_name)

	def get_my_followees(self):
		return self.api.friends(self.my_screen_name)
