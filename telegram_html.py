import os
import re
import bs4
from datetime import datetime
import chat_data_types as data
import filetype_tester as filetype
from urllib.parse import urlparse

# Get list of message files to parse
DIRECTORY = "demo/Telegram/html/2/"
message_regex = re.compile(r"^messages(\d)*.html")
filenames = [
    filename for filename in os.listdir(DIRECTORY) if message_regex.search(filename)
]


# Helper function
def date_telegram_to_iso(original_date: str) -> str:
    return datetime.strptime(original_date, r"%d.%m.%Y %H:%M:%S UTC%z").isoformat()


# Open each message file
for filename in [filenames[0]]:
    with open(DIRECTORY + f"/{filename}", encoding="utf-8") as file:
        # Initialize Chat Data
        chat = data.ChatData(
            format_revision=0,
            attributes=data.Attributes(
                platform=data.Platform.telegram_html,
                chat_name="",
                type=data.Type.direct,
                participants=[],
                file_path=os.path.abspath(file.name),
            ),
            messages=[],
        )

        # Parse file
        soup = bs4.BeautifulSoup(file, features="lxml")

        # Populate attributes
        chat.attributes.chat_name = (
            soup.find("div", class_="page_header")
            .find("div", class_="text")
            .text.strip()
        )

        author: str = ""
        authors: set[str] = set()
        # Find all messages
        for idx, message_element in enumerate(soup.find_all("div", class_="message")):
            # Initialize Message Data
            msg = data.Message(
                id=str(message_element["id"]),
                sequence=idx,
                timestamp=None,
                type=data.Type1.text,
                author="",
                body=None,
                context=None,
                attachments=[],
                reactions=[],
            )

            # Parse service messages
            if "service" in message_element["class"]:
                # Update message data
                msg.type = data.Type1.system
                msg.body = message_element.text.strip()
                author = ""

            # Parse user messages
            elif "default" in message_element["class"]:
                # Update timestamp
                timestamp_element = message_element.find(
                    "div", attrs={"class": ["date", "details"]}
                )
                if timestamp_element is not None:
                    msg.timestamp = date_telegram_to_iso(
                        str(timestamp_element["title"]).strip()
                    )

                # Update body
                body = message_element.find("div", class_="text")
                if body is not None:
                    msg.body = body.text.strip()

                # Update attachments
                media_element = message_element.find("div", class_="media_wrap")
                if media_element is not None:
                    msg.type = data.Type1.media
                    if media_element.find("div", class_="media_call") is not None:
                        print("CALL")
                    elif media_element.find("a", class_="media_location") is not None:
                        print(media_element.find("a").attrs["href"])
                    else:
                        attach = data.Attachment(url="", mime="")
                        fname = media_element.find("a").attrs["href"]
                        attach.url = os.path.abspath(DIRECTORY+str(fname))
                        attach.mime = filetype.check_mime(attach.url)
                        msg.attachments.append(attach)

                # Update author
                if (
                    author_element := message_element.find("div", class_="from_name")
                ) is not None:
                    new_author = author_element.text.strip()
                    author = new_author if new_author != author else author
                    authors.add(author)
                msg.author = author

            # Print
            chat.attributes.participants = [*authors]
            print(msg)
            # print(f"{msg.type.value}{(' ' if msg.author != "" else "") + msg.author}: {msg.body}")
            chat.messages.append(msg)

    #print(chat)
