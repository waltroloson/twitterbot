import tweepy

__author__ = 'Jacek Aleksander Gruca'


# This class provides persistence abstraction.
class TwitterApi(object):
	#
	def __init__(self, consumer_token, consumer_secret, access_token, access_token_secret):
		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	def follow(self, handles_to_follow):

		for handle_to_follow in handles_to_follow:
			print handle_to_follow
			if not self.is_followed_by_me(handle_to_follow):
				if not self.api.create_friendship(handle_to_follow):
					return False

		return True

	def unfollow(self, handles_to_unfollow):

		for handle_to_unfollow in handles_to_unfollow:
			if not self.api.destroy_friendship(handle_to_unfollow):
				return False

		return True

	def follows_me(self, handle):
		friendship = self.api.show_friendship(
			source_screen_name=str(self.api.me().screen_name),
			target_screen_name=handle)[0]

		print friendship
		return friendship.following

	def is_followed_by_me(self, handle):
		friendship = self.api.show_friendship(
			source_screen_name=str(self.api.me().screen_name),
			target_screen_name=handle)[0]

		print friendship
		return friendship.followed_by
