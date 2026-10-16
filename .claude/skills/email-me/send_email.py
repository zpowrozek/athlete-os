#!/usr/bin/env python3
import json, os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

ROOT = os.environ.get('ATHLETE_OS_ROOT', os.getcwd())
load_dotenv(os.path.join(ROOT, '.env'))

ADDRESS = os.getenv('GMAIL_ADDRESS')
APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')


def send_email(subject, html_body, to=None):
    if not ADDRESS or not APP_PASSWORD:
        raise RuntimeError('GMAIL_ADDRESS or GMAIL_APP_PASSWORD missing from .env')
    to = to or ADDRESS
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = ADDRESS
    msg['To'] = to
    msg.attach(MIMEText(html_body, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(ADDRESS, APP_PASSWORD)
        server.sendmail(ADDRESS, to, msg.as_string())


if __name__ == '__main__':
    payload = json.load(sys.stdin)
    send_email(payload['subject'], payload['html_body'], payload.get('to'))
    print(f"Sent to {payload.get('to') or ADDRESS}")
