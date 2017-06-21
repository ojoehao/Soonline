# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/13 下午8:38'
from random import Random
from django.core.mail import send_mail
from Soonline.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def send_register_email(email, send_typy="register"):
    emailVerifyRecord = EmailVerifyRecord()
    random_str = generate_random_str(16)
    emailVerifyRecord.code = random_str
    emailVerifyRecord.email = email
    emailVerifyRecord.send_type = send_typy
    emailVerifyRecord.save()

    if send_typy == "register":
        email_title = "luanluanmamamamamamamamama"
        email_body = "请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_typy == "forget" :
        email_title = "luanluanmamamamamamamamama"
        email_body = "请点击下面链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass



def generate_random_str(randomlength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

