from dateutil.relativedelta import relativedelta
from datetime import timedelta
from datetime import datetime

import sys

__author__ = 'Jacek Aleksander Gruca'


# This class contains the core of the TwitterBot logic as defined below.
# - Follow handles on a specific list.
# - Track when they were last followed.
# - Not follow anyone followed in the past year.
# - Not follow anyone already following my handle.
# - Unfollow the person after 30 days.
# - Process no more than 50 items in the queue per each invocation.
# - If already following a person that is not following my handle and they have not been followed
# in the past year: unfollow them and then re-follow them in 30 days.
class Handler(object):
	#
	def __init__(self, twitter_api, persistent_store, queue, batch_count, day_count):
		self.batch_count = batch_count
		self.day_count = day_count
		self.api = twitter_api
		self.store = persistent_store
		self.queue = queue
		self.time_now = None

	def delete_removed_items(self, handles):

		items_in_queue = self.queue.get_all_handles()
		items_to_remove = list(set(items_in_queue).difference(set(handles)))
		self.queue.remove_handles(items_to_remove)

	def append_added_items(self, handles):

		items_in_queue = self.queue.get_all_handles()
		items_to_add = set(handles).difference(set(items_in_queue))
		self.queue.append_handles(items_to_add)

	# this function is used to unfollow all handles after 30 days and to refollow
	# handles unfollowed-on-purpose
	def action_all_handles_marked_n_days_ago_or_more(self, action, property_name, day_count):

		past_date = self.time_now - timedelta(days=day_count)
		items_to_action = self.store.get_all_items_with_property_lte(property_name, past_date)
		action(items_to_action)

	def action_unfollow(self, items_to_action):

		for item in items_to_action:
			self.api.unfollow([item.handle])
			item.followed = False
			item.followed_on = None
			self.store.update_item(item)

	def action_follow(self, items_to_action):

		for item in items_to_action:
			self.api.follow([item.handle])
			item.followed = True
			item.followed_on = self.time_now
			self.store.update_item(item)

	def run(self, input_handles):

		# obtain the timestamp which will further on be considered as "now" until the end of this run
		self.time_now = datetime.now()

		# remove all items removed from the input file from the queue
		self.delete_removed_items(input_handles)

		# append all items added to the input file to the end of the queue
		self.append_added_items(input_handles)

		# unfollow all handles followed 30 days ago or more
		self.action_all_handles_marked_n_days_ago_or_more(
			self.action_unfollow, "followed_on", self.day_count)

		# follow all handles marked as unfollowed_on_purpose 30 days ago or more
		self.action_all_handles_marked_n_days_ago_or_more(
			self.action_follow, "unfollowed_on_purpose", self.day_count)

		handles_unfollowed_on_purpose = \
			[item['twitter_handle'] for item in self.store.get_all_items_with_property_lte(
				"unfollowed_on_purpose", self.time_now)]

		handles_followed_in_the_past_year = \
			[item['twitter_handle'] for item in self.store.get_all_items_with_property_gte(
				"followed_on", self.time_now - relativedelta(years=1))]

		handles_following_me = [item.screen_name for item in self.api.get_my_followers()]
		handles_i_follow = [item.screen_name for item in self.api.get_my_followees()]

		print "Handles followed in the past year:"
		print handles_followed_in_the_past_year
		print

		print "Handles unfollowed on purpose:"
		print handles_unfollowed_on_purpose
		print

		print "Handles following me:"
		print handles_following_me
		print

		print "Handles I follow:"
		print handles_i_follow
		print

		handles = self.queue.get_all_handles()
		print "Handles in the queue:"
		print handles
		print

		print "Carrying out periodic run."

		self.process_queue(handles, handles_followed_in_the_past_year, handles_following_me, handles_i_follow)

	def process_queue(self, handles, handles_followed_in_the_past_year, handles_following_me, handles_i_follow):

		i = 0
		for handle in handles:
			i += 1
			if i > self.batch_count:
				print "\nConcluding execution."
				break
			sys.stdout.write("\n%i / %i => " % (i, self.batch_count))
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
				print "I am following handle %s but they are not following me and they have not been followed" % handle + \
						" in the past year." \
						" Unfollowing, marking as unfollowed_on_purpose and adding to " + \
						"the back of the queue."
				self.api.unfollow([handle])
				self.store.mark_item(handle, 'unfollowed_on_purpose', self.time_now)
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				continue
			if self.api.requested_to_follow(handle):
				print "Already requested to follow %s." % handle
				self.queue.remove_handles([handle])
				self.queue.append_handles([handle])
				continue
			print "Following handle %s, marking as followed (followed_on=today) and adding to the back of the queue." \
					% handle
			self.api.follow([handle])
			self.store.mark_item(handle, 'followed', 'True')
			self.store.mark_item(handle, 'followed_on', self.time_now)
			self.queue.remove_handles([handle])
			self.queue.append_handles([handle])
