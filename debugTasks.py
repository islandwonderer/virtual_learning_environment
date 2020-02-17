import Gateway as gt
import dbModels as db
from threading import Thread
import time
import json


def add_teacher(first, last, t_id, email):
    teacher = db.dbUser(first, last, t_id, email)
    teacher.set_auto_user_name()
    teacher.set_custom_password("TestPass")
    teacher.isTeacher = True
    gt.gateway_ses.add(teacher)
    gt.gateway_ses.commit()


def clear_db():
    for user in gt.gateway_ses.query(db.dbUser):
        if not user.isTeacher:
            gt.gateway_ses.delete(user)
    for vm in gt.gateway_ses.query(db.dbComputer):
        gt.gateway_ses.delete(vm)
    gt.gateway_ses.commit()
    for user in gt.gateway_ses.query(db.dbUser):
        print(user)
    for vm in gt.gateway_ses.query(db.dbComputer):
        print(vm)


def display_db():
    print("Current DB")
    for user in gt.gateway_ses.query(db.dbUser):
        print(user)
    for vm in gt.gateway_ses.query(db.dbComputer):
        print(vm)


def check_status(this_instance):
    global instanceIsReady
    this_instance.is_instance_ready()
    instanceIsReady = True
    return


def count_while_we_wait():
    i = 1
    while instanceIsReady is False:
        print(i)
        time.sleep(10)
        i += 1
    return


def thread_task():
    t1 = Thread(target=check_status)
    t2 = Thread(target=count_while_we_wait)

    t1.start()
    t2.start()

#
# teacher = db.dbUser("Eva", "Longoria", 1234567, "faketest@psudomail.com")
# teacher.isTeacher = True
# teacher.setAutoUserName()
# teacher.setCustPassword("TestPass")
# gt.gateway_ses.add(teacher)
# gt.gateway_ses.commit()

# clear_db()
# display_db()
# thread_tasks()
# update_config()


# teacher = gt.user_by_id(31415926)
# teacher.isTeacher = True
# teacher.isSuspended = False
# gt.gateway_ses.add(teacher)
# gt.gateway_ses.commit()

# firstName = "Gabe"
# usefirstName = "Roberto"
# uselastName = "Bartholomew"
# usedate_stamp = "Feb.24,2019"
#
# message = "{},\n The following is to notify you that {} {} accessed your VM on {}. If something has changed in" \
#                   "your configuration notify an instructor at your earliest continence.".format(firstName, usefirstName, uselastName, usedate_stamp)
#
#
# print(message)

# 13009691
# test_user = gt.user_by_id(13009691)
# print(test_user.assigned_VM)
# test_vm = gt.get_vm_object(test_user.assigned_VM)
# log = test_vm.getLog()
# print(log)
#
# def clear_all():
#     for user in gt.gateway_ses.query(db.dbUser):
#         gt.gateway_ses.delete(user)
#
# add_teacher("Lady", "Longoria", 1234567, "mendo@lala.land")
# clear_db()
display_db()

