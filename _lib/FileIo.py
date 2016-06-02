import os
import csv
import re

__author__ = 'Jacek Aleksander Gruca'


# This class provides CSV processing functions to code in which we want to abstract this processing out.
class FileIo(object):

	def __init__(self, field_names):
		self.fieldNames = field_names

	def get_file_as_rows(self, filename, leading_column):
		lines = []
		with open(filename) as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=self.fieldNames)
			next(reader, None)  # skip the headers
			for row in reader:
				lines.append(row)
		return filter(lambda x: x[leading_column], lines)
