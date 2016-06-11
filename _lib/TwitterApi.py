import csv
import pandas

__author__ = 'Jacek Aleksander Gruca'


# This class provides persistence abstraction.
class TwitterApi(object):
	#
	def unfollow(self, handles_to_unfollow):
		return

	def follows_me(self, handle):
		return False

	def is_followed_by_me(self, handle):
		return True
