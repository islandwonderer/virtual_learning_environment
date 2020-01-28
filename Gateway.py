import smtplib
import dbModels as db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dbModels import Session
import json
import datetime as dt
import bcrypt

# Setup
default_password = "Capstone2019"
default_address = "testgrpython@gmail.com"
default_smtp = "smtp.gmail.com"
default_port = 587

gateway_ses = Session()


# VM Management
def create_vm(ami):
    new_instance = db.dbComputer(ami)
    gateway_ses.add(new_instance)
    gateway_ses.commit()
    return new_instance


def get_vm_object(vm_id):
    for vm in gateway_ses.query(db.dbComputer):
        if vm.InstanceId == vm_id:
            return vm
    return None


def del_vm(vm_obj):
    vm_obj.deleteInstace()
    gateway_ses.delete(vm_obj)
    gateway_ses.commit()


# Session Management
def verify_session(username, password):
    for user in gateway_ses.query(db.dbUser):
        if user.studentID == username and bcrypt.checkpw(user.password.encode('utf-8'), password.encode('utf-8')):
            return True
    return False


def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file)


def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config


# User Management
def create_single_user(u_id, first, last, email, ami):
    if user_by_id(u_id) is None:
        new_user = db.dbUser(first, last, u_id, email)
        password = new_user.setAutoPassword()
        new_instance = create_vm(ami)
        new_user.assigned_VM = new_instance.InstanceId
        date_stamp = dt.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        start_log = {'Created': date_stamp}
        new_instance.setLog(start_log)
        new_user.setLog(start_log)
        gateway_ses.add(new_user)
        gateway_ses.add(new_instance)
        gateway_ses.commit()
        message = "{}, \nThis message is about your account for 158.120's class gateway, refer to class sylabus for site. " \
                  "To login use your student ID and this password '{}'.\n Wishing you a good year:\n " \
                  "The Teaching Staff".format(new_user.firstName, password)
        subject = "158.120 Gateway Info for {}".format(new_user.firstName)
        success = notify_user(new_user, message, subject)
        return success


def user_by_id(u_id):
    for user in gateway_ses.query(db.dbUser):
        if user.studentID == u_id:
            return user
    return None


def user_by_name(name):
    for user in gateway_ses.query(db.dbUser):
        if user.firstName == name:
            return user
    return None


def get_list_users():
    user_list = []
    for user in gateway_ses.query(db.dbUser):
        user_list.append(user)
    user_list.sort(key=lambda e: e.lastName)
    print(user_list)
    return user_list


def save_user(user):
    gateway_ses.add(user)
    gateway_ses.commit()


def del_user(user):
    gateway_ses.delete(user)
    gateway_ses.commit()


def notify_user(user, message, subject):
    e_mail = smtplib.SMTP(host=default_smtp, port=default_port)
    msg = MIMEMultipart()
    msg['From'] = default_address
    msg['To'] = user.eMail
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    e_mail.connect(default_smtp, default_port)
    e_mail.ehlo()
    e_mail.starttls()
    e_mail.ehlo()
    try:
        e_mail.login(default_address, default_password)
        e_mail.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        e_mail.quit()
        return "Fail"
    e_mail.quit()
    del msg

