#!/usr/bin/python3

"""
Markdown script using python.
This script converts a Markdown file to an HTML file by parsing various Markdown syntax.
"""

import sys  # Import the sys module for command-line argument handling
import os.path  # Import os.path for file path operations
import re  # Import the re module for regular expression matching
import hashlib  # Import hashlib for generating hash values

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    # Check if the input Markdown file exists
    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    # Open the input Markdown file for reading and the output HTML file for writing
    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            # Flags to track the state of unordered/ordered lists and paragraph handling
            unordered_start, ordered_start, paragraph = False, False, False
            
            # Loop through each line in the Markdown file
            for line in read:
                # Replace bold syntax '**text**' with HTML <b> tags
                line = line.replace('**', '<b>', 1)  # Replace the first occurrence of '**' with '<b>'
                line = line.replace('**', '</b>', 1)  # Replace the second occurrence of '**' with '</b>'
                line = line.replace('__', '<em>', 1)  # Replace the first occurrence of '__' with '<em>'
                line = line.replace('__', '</em>', 1)  # Replace the second occurrence of '__' with '</em>'

                # Handle the custom Markdown pattern for MD5 hash
                md5 = re.findall(r'\[\[.+?\]\]', line)  # Find patterns like [[text]]
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)  # Extract the text inside the [[ ]]
                if md5:  # If the pattern exists
                    # Replace the pattern with its MD5 hash
                    line = line.replace(md5[0], hashlib.md5(md5_inside[0].encode()).hexdigest())

                # Handle the custom pattern for removing the letter 'C'
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)  # Find patterns like ((text))
                remove_c_more = re.findall(r'\(\((.+?)\)\)', line)  # Extract the text inside the (( ))
                if remove_letter_c:  # If the pattern exists
                    # Remove the letter 'C' from the extracted text
                    remove_c_more = ''.join(c for c in remove_c_more[0] if c not in 'Cc')
                    line = line.replace(remove_letter_c[0], remove_c_more)

                # Calculate line length and identify headings and list items
                length = len(line)
                headings = line.lstrip('#')  # Strip '#' characters to get the heading text
                heading_num = length - len(headings)  # Count the number of '#' characters
                unordered = line.lstrip('-')  # Check for unordered list items
                unordered_num = length - len(unordered)  # Count the number of '-' characters
                ordered = line.lstrip('*')  # Check for ordered list items
                ordered_num = length - len(ordered)  # Count the number of '*' characters
                
                # Process headings (1-6) by converting to HTML <h1> to <h6>
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

                # Process unordered list items
                if unordered_num:
                    if not unordered_start:  # If starting a new unordered list
                        html.write('<ul>\n')  # Open <ul> tag
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'  # Convert list item to <li>

                # Close unordered list if the line does not continue the list
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')  # Close <ul> tag
                    unordered_start = False

                # Process ordered list items
                if ordered_num:
                    if not ordered_start:  # If starting a new ordered list
                        html.write('<ol>\n')  # Open <ol> tag
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'  # Convert list item to <li>

                # Close ordered list if the line does not continue the list
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')  # Close <ol> tag
                    ordered_start = False

                # Process paragraphs
                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:  # If starting a new paragraph
                        html.write('<p>\n')  # Open <p> tag
                        paragraph = True
                    elif length > 1:  # If continuing a paragraph
                        html.write('<br/>\n')  # Insert a line break
                    elif paragraph:  # If ending the paragraph
                        html.write('</p>\n')  # Close <p> tag
                        paragraph = False

                # Write the processed line to the HTML file if it's not empty
                if length > 1:
                    html.write(line)

            # Close any open lists or paragraphs at the end of the file
            if unordered_start:
                html.write('</ul>\n')  # Close <ul> tag if it was open
            if ordered_start:
                html.write('</ol>\n')  # Close <ol> tag if it was open
            if paragraph:
                html.write('</p>\n')  # Close <p> tag if it was open

exit(0)  # Exit the script successfully
