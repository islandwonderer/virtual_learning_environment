# Imported Packages
import json
import datetime as dt
import bcrypt
import time

# Local Imports
from controller_and_modules import DatabaseModule as dB
from controller_and_modules.DatabaseModule import Session
from controller_and_modules.EmailModule import EmailModule as eM


# Setup
gateway_ses = Session()
mail_it = eM()
config_file = "controller_and_modules/config.json"


# VM Management
def create_vm():
    sc = load_config()
    new_instance = dB.dbComputer(sc["AMI"], sc["instance_type"], sc["key_name"], [sc["security_group_id"]])
    gateway_ses.add(new_instance)
    gateway_ses.commit()
    return new_instance


def get_vm_object(vm_id):
    for vm in gateway_ses.query(dB.dbComputer):
        if vm.InstanceId == vm_id:
            return vm
    return None


def del_vm(vm_obj):
    vm_obj.delete_instance()
    gateway_ses.delete(vm_obj)
    gateway_ses.commit()


# Session Management
def verify_user(username, password):
    for user in gateway_ses.query(dB.dbUser):
        if user.studentID == username and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True
    return False


def save_config(config):
    with open(config_file, 'w') as file:
        json.dump(config, file)


def load_config():
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


# User Management
def create_single_user(u_id, first, last, email):
    if user_by_id(u_id) is None:
        new_user = dB.dbUser(first, last, u_id, email)
        password = new_user.set_auto_password()
        new_instance = create_vm()
        new_user.assigned_VM = new_instance.InstanceId
        date_stamp = dt.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        start_log = {'Created': date_stamp}
        instance_log = {'Created': date_stamp,'Start Time': time.time(), 'On Time': []}
        new_instance.set_log(instance_log)
        new_user.set_log(start_log)
        gateway_ses.add(new_user)
        gateway_ses.add(new_instance)
        gateway_ses.commit()
        message = "{}, \nThis message is about your account for 158.120's class gateway, refer to class sylabus for site. " \
                  "To login use your student ID and this password '{}'.\n Wishing you a good year:\n " \
                  "The Teaching Staff".format(new_user.firstName, password)
        subject = "158.120 Gateway Info for {}".format(new_user.firstName)
        success = notify_user(new_user, message, subject)
        return new_user, success


def user_by_id(u_id):
    for user in gateway_ses.query(dB.dbUser):
        if user.studentID == u_id:
            return user
    return None


def user_by_name(name):
    for user in gateway_ses.query(dB.dbUser):
        if user.firstName == name:
            return user
    return None


def get_list_users():
    user_list = []
    for user in gateway_ses.query(dB.dbUser):
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
    config = load_config()
    email_address = user.eMail
    result = mail_it.send_mail(email_address, message, subject, config)
    return result
