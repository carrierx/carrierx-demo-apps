import os
import smtplib
import sys
from configparser import ConfigParser
from flexml_project import settings


def send_email(subject: str, to_addr: str, body_text: str):
    """
    Send an email
    """

    config_path = os.path.join(settings.BASE_DIR, "email.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    host = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "from_addr")
    BODY = "\r\n".join((
        f"From: {from_addr}",
        f"To: {to_addr}",
        f"Subject: {subject}",
        "",
        body_text
    ))
    server = smtplib.SMTP(host, port=int(port))
    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()

