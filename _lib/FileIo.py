import csv

__author__ = 'Jacek Aleksander Gruca'


# This class provides file processing functions including CSV processing.
class FileIo(object):
	#
	def __init__(self, field_names):
		self.field_names = field_names

	def get_file_as_rows(self, filename, leading_column):
		lines = []
		with open(filename) as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=self.field_names)
			next(reader, None)  # skip the header
			for row in reader:
				lines.append(row)
		return filter(lambda x: x[leading_column], lines)
