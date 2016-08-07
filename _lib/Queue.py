from pymongo import MongoClient

__author__ = 'Jacek Aleksander Gruca'


# This class abstracts the queue stored in the underlying database.
class Queue(object):
	#
	def __init__(self, host, port):
		self.client = MongoClient(host, port)
		self.db = self.client['twitterbot']
		self.queue = self.client.twitterbot['queue']

	def get_all_handles(self):
		handles = []
		for item in self.queue.find():
			handles.append(item['twitter_handle'])
		return handles

	def remove_handles(self, handles_to_remove):
		for handle in handles_to_remove:
			self.queue.delete_one({'twitter_handle': handle})

	def append_handles(self, handles_to_append):
		for handle in handles_to_append:
			self.queue.insert({'twitter_handle': handle})
