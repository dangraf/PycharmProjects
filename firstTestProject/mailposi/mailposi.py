import smtplib
from email.mime.text import MIMEText
import configparser
import random

class Settings:
    def __init__(self):
        self.parameters = None
        self.loadSettings()

    def loadSettings(self):
        try:
            self.parameters = configparser.ConfigParser()
            self.parameters.read('credentials.txt')
        except:
            print('error loadSettings in mailposi.py')
            pass
    def composeTextMsg(self):
        sections = self.parameters.sections()
        sections.remove('settings')
        sections.remove('maillist')
        text = ""

        for sec in sections:
            options = self.parameters.options(sec)
            idx = random.randint(0, len(options)-1)
            text = text + self.parameters.get(sec,options[idx]) + " \n \n"

            # generate a random number between 0 and len(options)


        return text


    def sendMail(self):
        me = self.parameters.get('settings','mailaddress')


        s = smtplib.SMTP(self.parameters.get('settings', 'popserver'),\
                         self.parameters.get('settings', 'port'))
        s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
        s.starttls()  # Puts connection to SMTP server in TLS mode
        s.ehlo()
        pwd = self.parameters.get('settings', 'passowrd')
        s.login(me, pwd)

        self.parameters.get('settings', 'passowrd')
        recepies = self.parameters.get('maillist', 'to').split(',')
        for receiver in recepies:
            msg = MIMEText(self.composeTextMsg())
            msg['Subject'] = 'Daily task'
            msg['From'] = me
            msg['To'] = receiver
            #s.sendmail(me, receiver, msg.as_string())
        s.quit()

set = Settings()
print( set.composeTextMsg() )