import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailModule:
    def __init__(self):
        self.default_password = ""
        self.default_address = ""
        self.default_smtp = ""
        self.default_port = ""

    def load_email_info(self, config):
        self.default_address = config["email"]
        self.default_password = config["e_password"]
        self.default_smtp = config["smtp"]
        self.default_port = config["port"]

    def send_mail(self, email_address, message, subject, config_dict):
        self.load_email_info(config_dict)
        e_mail = smtplib.SMTP(host=self.default_smtp, port=self.default_port)
        msg = MIMEMultipart()
        msg['From'] = self.default_address
        msg['To'] = email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        e_mail.connect(self.default_smtp, self.default_port)
        e_mail.ehlo()
        e_mail.starttls()
        e_mail.ehlo()
        try:
            e_mail.login(self.default_address, self.default_password)
            e_mail.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            e_mail.quit()
            return False
        e_mail.quit()
        del msg
        return True
