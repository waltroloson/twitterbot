import argparse
import pandas

from _lib.Handler import Handler

__author__ = 'Jacek Aleksander Gruca'

doc = '''
Welcome to TwitterBot. This automaton follows Twitter handles according to logic specified in the README file.
'''

parser = argparse.ArgumentParser(description=doc)
parser.add_argument('INPUT_FILE', action='store', help='read handles from input file')

args = parser.parse_args()

df = pandas.read_csv(args.INPUT_FILE)
handles = df[pandas.notnull(df.Twitter)].Twitter.values.tolist()

handler = Handler()
handler.run(handles)
