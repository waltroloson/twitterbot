from pymongo import MongoClient

__author__ = 'Jacek Aleksander Gruca'


# This class provides persistence abstraction for storing information about Twitter handles processed.
class PersistentStore(object):
	#
	def __init__(self, uri):
		self.client = MongoClient(uri)
		self.db = self.client['twitterbot']
		self.allhandles = self.client.twitterbot['allhandles']

	def get_all_items(self):
		items = []
		for item in self.allhandles.find():
			items.add(item)
		return items

	def get_all_items_with_property_lte(self, property_key, property_value):
		return list(self.allhandles.find({property_key: {"$lt": property_value}}))

	def get_all_items_with_property_gte(self, property_key, property_value):
		return list(self.allhandles.find({property_key: {"$gt": property_value}}))

	def mark_item(self, handle, property_name, property_value):
		item = self.allhandles.find_one({'twitter_handle': handle})
		item[property_name] = property_value
		self.allhandles.update({'twitter_handle': handle}, {"$set": item})

	def add_item(self, handle):
		if not self.allhandles.find_one({'twitter_handle': handle}):
			self.allhandles.insert_one({'twitter_handle': handle})

	def update_item(self, item):
		if self.allhandles.find_one({'twitter_handle': item.handle}):
			self.allhandles.update({'twitter_handle': item.handle}, {"$set": item}, upsert=False)
