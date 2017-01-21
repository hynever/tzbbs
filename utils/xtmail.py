#coding: utf8

from exts import mail
from threading import Thread
from flask_mail import Message
import config
from captcha.xtcaptcha import Captcha
from utils import xtcache


class XTMailType(object):
    MAIL_CAPTCHA = 0

class XTMail(object):

    def __init__(self,mail_type):
        self.mail_type = mail_type
        self.emails = []

    def send_mail(self,email):
        self.send_mails([email])

    def send_mails(self,emails):
        self.emails = emails
        if self.mail_type == XTMailType.MAIL_CAPTCHA:
            self.__send_captcha_mail__()


    def __send_captcha_mail__(self):
        msg = Message(u'Python潭州学院论坛邮箱验证码', recipients=self.emails)
        captcha = Captcha.gene_text()
        xtcache.set(captcha.lower(), captcha.lower())
        msg.body = u'邮箱验证码是：%s' % captcha
        mail.send(msg)
