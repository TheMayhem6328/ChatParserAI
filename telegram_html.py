import os
import re
import bs4
from datetime import datetime
import chat_data_types as cdt

# Get list of message files to parse
DIRECTORY = "demo\\Telegram\\html\\1"
message_regex = re.compile(r"^messages(\d)*.html")
filenames = [
    filename for filename in os.listdir(DIRECTORY) if message_regex.search(filename)
]


# Helper function
def date_telegram_to_iso(original_date: str) -> str:
    dt = datetime.strptime(original_date, r"%d.%m.%Y %H:%M:%S UTC%z")
    return dt.isoformat()


# Open each message file
for filename in [filenames[0]]:
    with open(DIRECTORY + f"\\{filename}", encoding="utf-8") as file:
        # Initialize Chat Data
        chat = cdt.ChatData(
            format_revision=0,
            attributes=cdt.Attributes(
                platform=cdt.Platform.telegram_html,
                chat_name="",
                type=cdt.Type.direct,
                participants=[],
                file_path="",
            ),
            messages=[],
        )

        # Parse file
        soup = bs4.BeautifulSoup(file, features="lxml")

        # Populate attributes
        chat.attributes.file_path = os.path.abspath(file.name)
        chat.attributes.chat_name = (
            soup.find("div", attrs={"class": ["page_header"]})
            .find("div", attrs={"class": ["text"]})
            .text.strip()
        )

        # Find all messages
        for idx, element in enumerate(
            soup.find_all("div", attrs={"class": ["message"]})
        ):
            # Initialize Message Data
            msg = cdt.Message(
                id=str(element["id"]),
                sequence=idx,
                timestamp=None,
                type=cdt.Type1.text,
                author="",
                body=None,
                context=None,
                attachments=[],
                reactions=[],
            )

            # Parse service messages
            if "service" in element["class"]:
                # Update message data
                msg.type = cdt.Type1.system
                msg.body = element.text.strip()

            # Parse user messages
            elif "default" in element["class"]:
                # Update timestamp
                timestamp_element = element.find(
                    "div", attrs={"class": ["date", "details"]}
                )
                if timestamp_element is not None:
                    msg.timestamp = date_telegram_to_iso(
                        str(timestamp_element["title"]).strip()
                    )

                # Update body
                body = element.find("div", attrs={"class": ["text"]})
                if body is not None:
                    msg.body = body.text.strip()

            # Print
            print(msg.model_dump())
            chat.messages.append(msg)

    print(chat)