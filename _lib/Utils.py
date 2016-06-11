__author__ = 'Jacek Aleksander Gruca'


# This class provides file processing functions including CSV processing.
class Utils(object):
	#
	@staticmethod
	def get_column(dict_list, column_name):
		column = []
		for v in dict_list:
			column.append(v[column_name])
		return column
