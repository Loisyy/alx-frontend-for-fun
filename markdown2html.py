#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path

if __name__ == '__main__':
    # Check if the number of arguments is less than 3
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    # Check if the markdown file exists
    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    # If no issues, exit successfully
    exit(0)
