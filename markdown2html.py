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

    # Open the Markdown file and the output HTML file
    with open(sys.argv[1], 'r') as md_file, open(sys.argv[2], 'w') as html_file:
        for line in md_file:
            # Remove any leading/trailing whitespace
            line = line.strip()

            # Parse headings
            length = len(line)
            headings = line.lstrip('#')
            heading_num = length - len(headings)

            # If the line starts with 1-6 '#' characters, it's a heading
            if 1 <= heading_num <= 6:
                line = '<h{}>'.format(heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

            # Write the converted line to the HTML file
            html_file.write(line)

    # If no issues, exit successfully
    exit(0)
