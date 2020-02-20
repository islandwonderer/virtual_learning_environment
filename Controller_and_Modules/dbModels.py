# This file contains the objects to be used in conjunction with SQLAlchemy
import string
import random
import boto3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import time
import bcrypt

engine = create_engine('sqlite:///gateway.db', echo=True)
Base = declarative_base()
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
Session = sessionmaker(bind=engine)


class dbUser(Base):
    # Use set functions to create these based on the need
    __tablename__ = "dbUser"
    userName = Column('username', Integer, primary_key=True)
    password = Column('password', String(16), unique=True)
    firstName = Column('firstname', String(20), nullable=False)
    lastName = Column('lastname', String(20), nullable=False)
    eMail = Column('email', String(20), nullable=False)
    studentID = Column('id', Integer, unique=True)
    assigned_VM = Column('userVM', String, ForeignKey('dbComputer.InstanceIpAddress'))
    isTeacher = Column('teacher', Boolean, default=False)
    isSuspended = Column('suspended', Boolean, default=False)
    visitorsLog = Column('vLog', String)

    def __repr__(self):
        return f"User('{self.userName}', '{self.firstName}', '{self.lastName}', '{self.assigned_VM}')"

    def __init__(self, fN, lN, ID, eM = None):
        self.firstName = fN
        self.lastName = lN
        self.studentID = ID
        self.eMail = eM
        self.userName = self.studentID

    # This function creates a user_name from the student ID
    def set_auto_user_name(self):
        self.userName = self.studentID

    # This function creates a random password of 8 characters.
    def set_auto_password(self, size = 8, chars=string.ascii_letters + string.digits + string.punctuation):
        unencrypted_password = ''.join(random.choice(chars) for _ in range(size))
        salt = bcrypt.gensalt()
        hatch = bcrypt.hashpw(unencrypted_password.encode('utf-8'), salt)
        self.password = hatch
        return unencrypted_password

    def set_custom_user_name(self, uN):
        self.userName = uN

    def set_custom_password(self, pW):
        salt = bcrypt.gensalt()
        hatch = bcrypt.hashpw(pW.encode('utf-8'), salt)
        self.password = hatch

    def set_suspension(self, bool):
        self.isSuspended = bool

    def set_teacher(self, bool):
        self.isTeacher = bool

    def get_suspension(self):
        return self.isSuspended

    def get_teacher(self):
        return self.isTeacher

    def get_password(self):
        return self.password

    def get_user_name(self):
        return self.userName

    def get_log(self):
        return json.loads(self.visitorsLog)

    def set_log(self, dict_json):
        self.visitorsLog = json.dumps(dict_json)

    def add_to_log(self, key, value):
        dict_log = self.get_log()
        dict_log[key] = value
        self.set_log(dict_log)


class dbComputer(Base):
    __tablename__ = "dbComputer"
    InstanceId = Column('instanceId', String, primary_key=True)
    InstanceIpAddress = Column('InstanceIpAddress', String)
    InstanceLog = Column('log', String)

    def __init__(self, aimID, type, key, security_group):
        instance = ec2.create_instances(
            ImageId=aimID,
            MinCount=1,
            MaxCount=1,
            InstanceType=type,
            KeyName=key,
            SecurityGroupIds=security_group
        )
        self.instanceObject = instance[0]
        self.InstanceId = self.instanceObject.id

    def start_instance(self):
        client.start_instances(InstanceIds=[self.InstanceId])
        start = time.time()
        self.add_to_log("Start Time", start)

    def stop_instance(self):
        client.stop_instances(InstanceIds=[self.InstanceId])
        # end = time.time()
        log = self.get_log()
        end = time.time()
        start = log["Start Time"]
        duration = end - start
        if log["On Time"]:
            onTime = log["On Time"]
            onTime.append(duration)
            log["On Time"] = onTime
        self.set_log(log)

    def delete_instance(self):
        client.terminate_instances(InstanceIds=[self.InstanceId])

    def get_instance_ip(self):
        instance = ec2.Instance(self.InstanceId)
        self.InstanceIpAddress = instance.public_ip_address
        return self.InstanceIpAddress

    def get_instance_id(self):
        return self.InstanceId

    # Must implement some kind of timeout. /Check if function "wait" has a time out/
    def is_instance_ready(self):
        waiter = client.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=[self.InstanceId])
        return True

    def get_up_time(self):
        log = self.get_log()
        log_times = log["On Time"]
        total_up_time = 0
        for period in log_times:
            total_up_time += period
        return total_up_time

    def get_log(self):
        log = self.InstanceLog
        if log is not None:
            return json.loads(log)
        else:
            return {}

    def set_log(self, dict_json):
        self.InstanceLog = json.dumps(dict_json)

    def add_to_log(self, key, value):
        dict_log = self.get_log()
        dict_log[key] = value
        self.set_log(dict_log)

    def get_info(self):
        response = client.describe_instances(InstanceIds=[self.InstanceId])
        return response

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
