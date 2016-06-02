__author__ = 'Jacek Aleksander Gruca'

import argparse

from _lib.FileIo import FileIo
from _lib.Handler import Handler

FIELD_NAMES = ['Name', 'Job Title', 'Company', 'LinkedIn', 'Twitter', 'SIQ', 'Notes']

doc = '''
Welcome to TwitterBot. This automaton follows Twitter handles according to logic specified in the README file.
'''

parser = argparse.ArgumentParser(description=doc)
parser.add_argument('INPUT_FILE', action='store', help='read handles from input file')

args = parser.parse_args()

csvHelper = FileIo(FIELD_NAMES)
handler = Handler()

rows = csvHelper.get_file_as_rows(args.INPUT_FILE, 'Twitter')

for row in rows:
	print repr(row)

handler.run(row['Twitter'])
