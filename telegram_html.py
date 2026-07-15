import os
import re
import bs4

# Get list of files to import
DIRECTORY = "demo\\Telegram\\html\\1"
message_regex = re.compile(r"^messages(\d)*.html")
filenames = [filename for filename in os.listdir(DIRECTORY) if message_regex.search(filename)]

# Import HTML to memory
raw_html_contents = []
for filename in filenames:
    temp_content = ""
    with open(DIRECTORY+f"\\{filename}", encoding="utf-8") as file:
        temp_content = file.read()
        raw_html_contents.append(temp_content)

raw_html_content = raw_html_contents[0]
