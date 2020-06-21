import yagmail
import datetime
from secrets import RECEIVER, SENDER, PASSWORD


class EmailResults:
    def __init__(self):
        self.sender = SENDER
        self.receiver = RECEIVER
        self.password = PASSWORD
        self.body = "Version of the parsing results file for the date: " + datetime.datetime.now().strftime("%d-%m-%Y "
                                                                                                            "%H:%M")

    def send_file(self, filename):
        yag = yagmail.SMTP(self.sender, self.password)
        yag.send(
            to=self.receiver,
            subject="Site parsing results of a well-known trading platform",
            contents=self.body,
            attachments=filename,
        )

