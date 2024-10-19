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
        unordered_start = False  # Keep track of unordered list state
        
        for line in md_file:
            # Remove any leading/trailing whitespace
            line = line.strip()

            # Parse headings
            length = len(line)
            headings = line.lstrip('#')
            heading_num = length - len(headings)

            unordered = line.lstrip('-')
            unordered_num = length - len(unordered)

            # If the line starts with 1-6 '#' characters, it's a heading
            if 1 <= heading_num <= 6:
                line = '<h{}>'.format(heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

            # Parse unordered list items
            if unordered_num:
                if not unordered_start:
                    html_file.write('<ul>\n')
                    unordered_start = True
                line = '<li>' + unordered.strip() + '</li>\n'

            if unordered_start and not unordered_num:
                html_file.write('</ul>\n')
                unordered_start = False

            # Write the converted line to the HTML file
            html_file.write(line)

        # Close any open unordered list at the end of the file
        if unordered_start:
            html_file.write('</ul>\n')

    # If no issues, exit successfully
    exit(0)
