from pymongo import MongoClient

__author__ = 'Jacek Aleksander Gruca'


# This class provides persistence abstraction.
class PersistentStore(object):
	#
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.test

	def get_all_items(self):
		return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	def get_all_items_with_property_lte(self, property_key, property_value):
		return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	def get_all_items_with_property_gte(self, property_key, property_value):
		return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']

	def mark_item(self, handle, property_name, property_value):
		return True
