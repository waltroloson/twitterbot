from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from _lib.Queue import Queue
from _lib.PersistentStore import PersistentStore

__author__ = 'Jacek Aleksander Gruca'


class Handler(object):
	#
	def __init__(self, twitter_api, batch_count, day_count):
		self.batch_count = batch_count
		self.day_count = day_count
		self.api = twitter_api
		self.store = PersistentStore()
		self.queue = Queue()

	def delete_removed_items(self, handles):

		items_in_queue = self.queue.get_all_handles()
		items_to_remove = list(set(items_in_queue).difference(set(handles)))
		self.queue.remove_handles(items_to_remove)

	def append_added_items(self, handles):

		items_in_queue = self.queue.get_all_handles()
		items_to_add = set(handles).difference(set(items_in_queue))
		self.queue.append_handles(items_to_add)

	def unfollow_all_handles_marked_in_last_n_days(self, property_name, day_count):

		past_date = datetime.now() - timedelta(days=day_count)
		items_to_unfollow = self.store.get_all_items_with_property_lte(property_name, past_date)

		self.api.unfollow([item.handle for item in items_to_unfollow])
		for item in items_to_unfollow:
			item.followed = False
			item.followed_on = None
			self.store.update_item(item)

	def run(self, input_handles):

		self.delete_removed_items(input_handles)
		self.append_added_items(input_handles)

		handles = self.queue.get_all_handles()

		self.unfollow_all_handles_marked_in_last_n_days("followed_on", self.day_count)
		self.unfollow_all_handles_marked_in_last_n_days("unfollowed_on_purpose", self.day_count)

		handles_followed_in_the_past_year = [item['twitter_handle'] for item in self.store.get_all_items_with_property_gte(
			"followed_on", datetime.now() - relativedelta(years=1))]

		handles_following_me = [item.screen_name for item in self.api.get_my_followers()]
		handles_i_follow = [item.screen_name for item in self.api.get_my_followees()]
		timeToday = datetime.now()

		print "Handles followed in the past year:"
		print handles_followed_in_the_past_year

		print "Handles following me:"
		print handles_following_me

		print "Handles I follow:"
		print handles_i_follow

		print "Carrying out daily run."

		i = 0

		print(handles)
		for handle in handles:
			self.store.add_item(handle)
			if handle in handles_followed_in_the_past_year:
				print "Handle %s followed in the past year, skipping and adding to the back of the queue." % handle
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				continue
			if handle in handles_following_me:
				print "Handle %s is following me, skipping and adding to the back of the queue." % handle
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				continue
			if handle in handles_i_follow:
				print "I am following handle %s. Unfollowing, marking as unfollowed-on-purpose and adding to " % handle \
						+ "the back of the queue."
				self.api.unfollow([handle])
				self.store.mark_item(handle, 'unfollowed_on_purpose', timeToday)
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				continue
			if i >= self.batch_count:
				print "Concluding execution.."
				break
			if self.api.requested_to_follow(handle):
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				"Already requested to follow %s." % handle
				break
			self.api.follow([handle])
			i += 1
			self.store.mark_item(handle, 'followed', 'True')
			self.store.mark_item(handle, 'followed_on', timeToday)
			self.queue.remove_handles([handle])
			self.queue.append_handles([handle])

# a. Check if the handle taken from the queue was followed in the past year. If yes: discard, add to the back of the
# queue, and take another item from the queue head.
# a. Check if the handle taken from the queue follows my handle. If yes: discard, add to the back of the queue, and
# take another item from the queue head.
# a. Check if we are already following that handle. If yes then:
#   i. unfollow that handle and mark as unfollowed-on-purpose,
#   i. add it to the back of the queue,
#   i. take another item from the queue head.

# a. Check if already followed 50 handles today. If yes: conclude execution.
# a. Follow that handle.
# a. Add that handle to the back of the queue.
# a. Take another item from the queue head and repeat.

# ___________ original requirements __________
# - Follow handles on a specific list
# - Track when they were last followed
# - Not follow anyone followed in the past year
# - Not follow anyone already following my handle
# - Unfollow the person after 30 days
# - Limit follows per day to 50
# - If already following a person that is not following my handle and
# they have not been followed in the past year, unfollow them and then
# re-follow them in 30 days
