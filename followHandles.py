import argparse

from _lib.FileIo import FileIo
from _lib.Handler import Handler
from _lib.Utils import Utils

__author__ = 'Jacek Aleksander Gruca'

FIELD_NAMES = ['Name', 'Job Title', 'Company', 'LinkedIn', 'Twitter', 'SIQ', 'Notes']

doc = '''
Welcome to TwitterBot. This automaton follows Twitter handles according to logic specified in the README file.
'''

parser = argparse.ArgumentParser(description=doc)
parser.add_argument('INPUT_FILE', action='store', help='read handles from input file')

args = parser.parse_args()

fileIo = FileIo(FIELD_NAMES)
handler = Handler()

handles = Utils.get_column(fileIo.get_file_as_rows(args.INPUT_FILE, 'Twitter'), 'Twitter')

for handle in handles:
	print handle

handler.run(handles)
