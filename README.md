# Virtual Learning Environment

## Introduction
This prototype project allows a teacher to deploy and manage a 
cloud of AWS virtual machines for use within a teaching environment. 
The instructor may add users in bulk or one at a time. 
Adding a user to the software creates an AWS EC2 instance and 
notifies the student via email about their login information.
 
Saving the education organization money is also an essential part 
of this prototype. When a student logs into the software, the
application starts their assigned VM and provides an updated 
link to the machine. It also shuts down the instance when the
student logs out or closes the app. This system translates into
considerable savings in contrast with having the virtual asset 
powered on all the time. Eliminating the need for static IPs or 
dynamic routing for each VM also reduces the operational cost.

Note that this project is a proof of concept. 
Ideally, this project would be web-based. A web-hosted application
would allow a student to connect to their virtual learning 
environment from any device without needing to download or install
any software. Please read the recorded issue in Github for a more
comprehensive list of further
improvements to the code and program.

## Software Overview
### Teacher Interface 
![Teacher interface with 3 major sections](https://i.imgur.com/3k6cxSU.png)

1. Management Area
    * VMs- This section allows the teacher to perform several tasks on AWS instances such as:
        * Turn ALL On or Off
        * Check status of individual VMs
        * Download visitor logs
    * Users- This section allows the teacher to modify a user's information including:
        * Change personal information
        * Change password
        * Suspend and enable accounts
        * Visit student's VM
    * Settings- This section allows the teacher to save settings for:
        * Email communication
        * VM creation parameters such as AMI and security groups
2. Single User Creation
    * This section allows the teacher to add a single user by providing the following information:
        * Student ID - Must be a unique integer
        * EMail - Need to notify student of credentialing information
        * First Name
        * Last Name
    * Please note that all the information must be completed to create a new user. 
3. Bulk User Creation
    * This section allows the teacher to create multiple users using a CSV file.
    * Please see the example CSV file provided in the /samples folder of this project.
   
### Student Interface 
![Overview image of the student interface](https://i.imgur.com/HVD4zt6.png)

1. VM Control
    * This section allows the student to:
        * Start and stop their assigned VM
        * Monitor the starting progress
    * The student is notified when the connection is completed.
2. Links
    * Once the VM is up, this section provides the student with links to access the VM.
    * Links reflect the latest VM configuration.
3. Other Class VMs
    * This section allows a student to visit a classmate's VM.
    * Access to other VM's is limited to the front facing web page.
    * Visits to other VM's are logged in the DB and host computer.
    
## Helpful Notes
### Required Packages
* SQL Alchemy 1.3.10
* AWS Boto3 1.10.14
* BCrypt 3.1.7
* URLLib 3 1.25.6

Use the following command:
```commandline
pip install SQLAlchemy bcrypt boto3 urllib3
```
Please note that for Boto3 to work you will need to have a configured 
AWS CLI environment working on your computer.
Instructions on setting this up can be found
[here.](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

### Database
A sample database has been included for the purpose of software testing and evaluation. 
Included in the database are these two sample users:
* Teacher
    * User ID: 1234567
    * Password: TestPass
* Student
    * User ID: 7777777
    * Password: SevenSevens
    
### Configuration
A sample configuration file has been provided in the /samples folder of this project.
This sample file must be renamed "config.json" and placed in the /controller_and_modules
folder for the software to work properly.

### Contributing
As explained in the introductions this software is only a proof of concept. We (royal) 
welcome contributions that take this from a proof of concept to a full featured solution
for educational VM management. 

Please just follow the simple guidelines:

* When contributing to this repository, please first discuss the change you wish to make 
via issue, email, or any other method with the owners of this repository before making 
a change.
* In all interactions please be kind and respectful.


## License
   MIT License

   Copyright (c) 2020 Gabriel Ruiz  

   Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
