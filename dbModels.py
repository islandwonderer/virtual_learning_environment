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
    def setAutoUserName(self):
        self.userName = self.studentID

    # This function creates a random password of 8 characters.
    def setAutoPassword(self, size = 8, chars=string.ascii_letters + string.digits + string.punctuation):
        unencrypted_password = ''.join(random.choice(chars) for _ in range(size))
        salt = bcrypt.gensalt()
        hatch = bcrypt.hashpw(unencrypted_password.encode('utf-8'), salt)
        self.password = hatch
        return unencrypted_password

    def setCustUserName(self, uN):
        self.userName = uN

    def setCustPassword(self, pW):
        salt = bcrypt.gensalt()
        hatch = bcrypt.hashpw(pW.encode('utf-8'), salt)
        self.password = hatch

    def setSuspention(self, bool):
        self.isSuspended = bool

    def setTeacher(self, bool):
        self.isTeacher = bool

    def getSuspention(self):
        return self.isSuspended

    def getTeacher(self):
        return self.isTeacher

    def getPassword(self):
        return self.password

    def getUserName(self):
        return self.userName

    def getLog(self):
        return json.loads(self.visitorsLog)

    def setLog(self, dict_json):
        self.visitorsLog = json.dumps(dict_json)

    def addToLog(self, key, value):
        dict_log = self.getLog()
        dict_log[key] = value
        self.setLog(dict_log)


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

    def startInstance(self):
        client.start_instances(InstanceIds=[self.InstanceId])
        start = time.time()
        self.addToLog("Start Time", start)

    def stopInstance(self):
        client.stop_instances(InstanceIds=[self.InstanceId])
        # end = time.time()
        log = self.getLog()
        end = time.time()
        start = log["Start Time"]
        duration = end - start
        if log["On Time"]:
            onTime = log["On Time"]
            onTime.append(duration)
            log["On Time"] = onTime
        self.setLog(log)

    def deleteInstace(self):
        client.terminate_instances(InstanceIds=[self.InstanceId])

    def getInstaceIP(self):
        instance = ec2.Instance(self.InstanceId)
        self.InstanceIpAddress = instance.public_ip_address
        return self.InstanceIpAddress

    def getInstaceID(self):
        return self.InstanceId

    # Must implement some kind of timeout. /Check if function "wait" has a time out/
    def isInstanceReady(self):
        waiter = client.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=[self.InstanceId])
        return True

    def getUpTime(self):
        log = self.getLog()
        logTimes = log["On Time"]
        totalUpTime = 0
        for period in logTimes:
            totalUpTime += period
        return totalUpTime

    def getLog(self):
        log = self.InstanceLog
        if log is not None:
            return json.loads(log)
        else:
            return {}

    def setLog(self, dict_json):
        self.InstanceLog = json.dumps(dict_json)

    def addToLog(self, key, value):
        dict_log = self.getLog()
        dict_log[key] = value
        self.setLog(dict_log)

    def getInfo(self):
        response = client.describe_instances(InstanceIds=[self.InstanceId])
        return response

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
