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
		self.queue = Queue()
		self.store = PersistentStore()

	def delete_removed_items(self, handles):

		items_in_queue = self.queue.get_all_items()
		items_to_remove = list(set(items_in_queue).difference(set(handles)))
		self.queue.remove_items(items_to_remove)

	def append_added_items(self, handles):

		items_in_queue = self.queue.get_all_items()
		items_to_add = set(handles).difference(set(items_in_queue))
		self.queue.append_items(items_to_add)

	def unfollow_all_handles_marked_in_last_n_days(self, property_name, day_count):

		past_date = datetime.now() - timedelta(days=day_count)

		handles_to_unfollow = self.store.get_all_items_with_property_lte(property_name, past_date)
		self.api.unfollow(handles_to_unfollow)

	def run(self, handles):

		self.delete_removed_items(handles)
		self.append_added_items(handles)
		self.unfollow_all_handles_marked_in_last_n_days("followed_on", self.day_count)
		self.unfollow_all_handles_marked_in_last_n_days("unfollowed_on_purpose", self.day_count)

		items_followed_in_the_past_year = self.store.get_all_items_with_property_gte(
			"followed_on", datetime.now() - relativedelta(years=1))

		i = 1

		for handle in handles:
			if handle in items_followed_in_the_past_year:
				self.queue.remove_items(handle)
				self.queue.append_items(handle)
				continue
			if self.api.follows_me(handle):
				self.queue.remove_items(handle)
				self.queue.append_items(handle)
				continue
			if self.api.is_followed_by_me(handle):
				self.api.unfollow(handle)
				self.store.mark_item(handle, 'unfollowed_on_purpose', True)
				self.queue.remove_items(handle)
				self.queue.append_items(handle)
				continue
			if i >= self.batch_count:
				print "Concluding execution.."
				break
			self.api.follow(handle)
			self.store.mark_item(handle, 'followed')
			self.queue.remove_items(handle)
			self.queue.append_items(handle)

		print "Carrying out daily run."

	# a. Check if the handle taken from the queue was followed in the past year. If yes: discard, add to the back of the queue, #and take another item from the queue head.
	# a. Check if the handle taken from the queue follows my handle. If yes: discard, add to the back of the queue, and take another item from the queue head.
	# a. Check if we are already following that handle. If yes then:
	#   i. unfollow that handle and mark as unfollowed-on-purpose,
	#   i. add it to the back of the queue,
	#   i. take another item from the queue head.

# a. Check if already followed 50 handles today. If yes: conclude execution.
# a. Follow that handle.
# a. Add that handle to the back of the queue.
# a. Take another item from the queue head and repeat.
