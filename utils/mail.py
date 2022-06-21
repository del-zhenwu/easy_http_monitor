# -*- coding: utf-8 -*-

import logging
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
from requests import post
from http_client import HttpClient

logger = logging.getLogger('easy_http.utils.mail')
SMS_DEFAULT_TO_LIST = [
    # "shiyujie@lianjia.com",
    "lizhenxiang@lianjia.com",
    # "linaiheng@lianjia.com",
    # "lvxiaochen001@lianjia.com",
    # "lichenglong004@lianjia.com",
]

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_email(subject, content, receivers=None):
    sender = 'lizhenxiang@lianjia.com'
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header("Online http-service alert")
    message['To'] = Header("easy_online")
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtp_obj = smtplib.SMTP('mail.lianjia.com')
        if receivers is None:
            receivers = SMS_DEFAULT_TO_LIST
        result = smtp_obj.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException as e:
        logger.error(str(e))


def send_email_sms(subject, content, receivers=None):
    if receivers is None:
        receivers = SMS_DEFAULT_TO_LIST
    data = {
        "version": "1.0",
        "method": "mail.sent",
        "group": "search",
        "auth": "DRNCOflatHrHj42Wn1MhMTy0jV7DzqPO",
        "params": {
            "to": receivers,
            "subject": subject,
            "body": content,
        }  
    }
    try:
        client = HttpClient("http://sms.lianjia.com")
        send_res = client.http_call("/lianjia/sms/send", post, data=data)
        logger.error("Send email success")
    except Exception as e:
        logger.error(str(e))
        logger.error("Send email failed")


if __name__ == '__main__':
    send_email("[mail test]", "test")
