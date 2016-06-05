__author__ = 'Jacek Aleksander Gruca'

import csv


# This class provides file processing functions including CSV processing.
class FileIo(object):
	#
	def __init__(self, field_names):
		self.fieldNames = field_names

	def get_file_as_rows(self, filename, leading_column):
		lines = []
		with open(filename) as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=self.fieldNames)
			next(reader, None)  # skip the header
			for row in reader:
				lines.append(row)
		return filter(lambda x: x[leading_column], lines)
