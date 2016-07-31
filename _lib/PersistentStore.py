from pymongo import MongoClient

__author__ = 'Jacek Aleksander Gruca'


# This class provides MongoDB persistence abstraction.
class PersistentStore(object):
	#
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['twitterbot']
		self.all_handles = self.client.twitterbot['allhandles']

	def get_all_items(self):
		items = []
		for item in self.all_handles.find():
			items.add(item)
		return items

	def get_all_items_with_property_lte(self, property_key, property_value):
		items = []
		for item in self.all_handles.find({property_key: {"$lt": property_value}}):
			items.add(item)
		return items

	def get_all_items_with_property_gte(self, property_key, property_value):
		return list(self.all_handles.find({property_key: {"$gt": property_value}}))

	def mark_item(self, handle, property_name, property_value):

		item = self.all_handles.find_one({'twitter_handle': handle})
		item[property_name] = property_value

		self.all_handles.update({'twitter_handle': handle}, {"$set": item})

	def add_item(self, handle):
		if not self.all_handles.find_one({'twitter_handle': handle}):
			self.all_handles.insert_one({'twitter_handle': handle})

	def update_item(self, item):
		if self.all_handles.find_one({'twitter_handle': item.handle}):
			self.all_handles.update({'twitter_handle': item.handle}, {"$set": item}, upsert=False)
