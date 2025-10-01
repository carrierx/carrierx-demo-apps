from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import sys
from configparser import ConfigParser
from flexml_project import settings


def get_email_body(recording_properties: dict):
    body: str = ""

    try:
        now = datetime.now()

        body: str = f"Hello,\n\nYou were left a {recording_properties['RecordingDuration']}s long voicemail on {recording_properties['To']} from {recording_properties['From']} on {now.strftime('%A, %B %d, %Y at %I:%M:%S %p')}.\n\nListen to the voicemail by clicking the following link:\n\n {recording_properties['RecordingUrl']}.{recording_properties['Storage_file_format']}"
    except:
        pass

    return body


def send_email(subject: str, to_addr: str, recording_properties: dict):
    """
    Send an email
    """

    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "email.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    host = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "from_addr")
    
    server = smtplib.SMTP(host, port=int(port))
    server.starttls()

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ", ".join([to_addr])
    msg["Subject"] = subject
    msg_body = get_email_body(recording_properties)
    msg.attach(MIMEText(msg_body))

    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
