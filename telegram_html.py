import os
import re
import bs4

# Get list of message files to parse
DIRECTORY = "demo\\Telegram\\html\\1"
message_regex = re.compile(r"^messages(\d)*.html")
filenames = [filename for filename in os.listdir(DIRECTORY) if message_regex.search(filename)]

# Open each message file
for filename in [filenames[0]]:
    with open(DIRECTORY+f"\\{filename}", encoding="utf-8") as file:
        # Parse file
        soup = bs4.BeautifulSoup(file, features="lxml")

        # Find all messages
        for element in soup.find_all("div", attrs={"class": ["message"]}):
            # Print service messages
            if "service" in element['class']:
                print("SVC:", element.text.strip())
            elif "default" in element['class']:
                text = element.find("div", attrs={"class": ["text"]})
                if text is not None:
                    print("USR:", text.text.strip())