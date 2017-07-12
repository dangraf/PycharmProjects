# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import configparser
import random
import schedule
import time


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
        # List all sections in the file
        # remove settings and mailing list that does not contain any questions
        sections = self.parameters.sections()
        sections.remove('settings')
        sections.remove('maillist')
        text = ""


        # iterate thrugh each section and radnomize a sentence within all options.
        for sec in sections:
            options = self.parameters.options(sec)
            idx = random.randint(0, len(options)-1)
            text = text +sec +':\n'
            text = text + '-'+ self.parameters.get(sec,options[idx]) + " \n \n"
        return text


    def sendMail(self):
        self.loadSettings()
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
            s.sendmail(me, receiver, msg.as_string())
        s.quit()

    def run(self):
        sendHour = str(self.parameters.get('maillist', 'sendhour'))
        while(1):
            schedule.every().day.at(sendHour).do(self.sendMail)
            time.sleep(60)



if __name__ == "__main__":
    set = Settings()
    set.run()
