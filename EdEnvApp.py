import webbrowser
import tkinter as tk
from tkinter import font as tkFont
import Gateway as gt
import csv
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from threading import Thread
import time

user = None
vm = None


class EdEnvApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, StudentPage, TeacherPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StudentPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login:", font=controller.title_font)
        label.pack()
        self.unEntry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.unEntry.insert(0, "Student ID")
        self.unEntry.pack()
        self.pwEntry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.pwEntry.insert(0, "Password")
        self.pwEntry.pack()
        self.login = tk.Button(self, text="Login", command=self.verify_login)
        self.login.pack()

    def verify_login(self):
        global user
        global vm
        user_id = int(self.unEntry.get())
        if gt.verify_session(user_id, self.pwEntry.get()):
            user = gt.user_by_id(user_id)
            if not user.isTeacher:
                vm = gt.get_vm_object(user.assigned_VM)
                print(vm.InstanceId)
                vm.startInstance()
                self.controller.show_frame("StudentPage")

            else:
                self.controller.show_frame("TeacherPage")
        else:
            messagebox.showinfo("Not Found", "Please Check Your Username And Password Then Try Again")


class StudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        stat_label = tk.Label(self, text="Student Interface:", font=controller.title_font)
        stat_label.grid(row=1, column=1, pady=5, padx=10, sticky=tk.NSEW)

        # Setup
        self.config = gt.load_config()
        self.moodle_site = ""
        self.php_my_admin_site = ""
        self.ftp_site = ""
        self.instanceIsReady = False
        self.waitTime = 240  # Four minutes

        # Start Section
        ins_label = tk.Label(self, text="Start Your VM Here")
        ins_label.grid(row=2, column=1, sticky="EW", padx=10)
        pro_label = tk.Label(self, text="Progress")
        pro_label.grid(row=2, column=2, sticky="W", padx=10)
        self.load_progress = Progressbar(self, orient='horizontal', length=165, mode='determinate')
        self.load_progress.grid(row=3, column=2, sticky="W", padx=10, pady=3)
        self.load_progress.place_forget()
        self.start_button = tk.Button(self, text="Start", command=self.start_check)
        self.start_button.grid(row=3, column=1, pady=3, padx=10)

        # Section Separation
        separator_line = Separator(self, orient="horizontal")
        separator_line.grid(row=4, column=1, columnspan=2, padx=15, pady=20, sticky="EW")

        # Sites Sections
        link_label = tk.Label(self, text="VM Links")
        link_label.grid(row=5, column=1, sticky='NSEW')
        self.moo_button = tk.Button(self, text="Moodle", command=lambda: self.open_page(self.moodle_site), state=tk.DISABLED)
        self.moo_button.grid(row=6, column=1, pady=15)
        self.moo_info = tk.Message(self, text=self.config['mood_info'], width=165, font=(None, 10))
        self.moo_info.grid(row=6, column=2, sticky=tk.W)
        self.php_button = tk.Button(self, text="phpAdmin", command=lambda: self.open_page(self.php_my_admin_site), state=tk.DISABLED)
        self.php_button.grid(row=7, column=1, pady=15)
        self.php_info = tk.Message(self, text=self.config['php_info'], width=165, font=(None, 10))
        self.php_info.grid(row=7, column=2, sticky=tk.W)
        self.ftp_button = tk.Button(self, text="FTP", command=lambda: self.open_page(self.ftp_site),  state=tk.DISABLED)
        self.ftp_button.grid(row=8, column=1, pady=15)
        self.ftp_info = tk.Message(self, text=self.config['ftp_info'], width=165, font=(None, 10))
        self.ftp_info.grid(row=8, column=2, sticky=tk.W)

    def set_ready(self):
        messagebox.showinfo("Ready", "Your instance is ready!")
        self.start_button.config(text="LogOut", command=lambda: self.log_out())
        self.start_button.config(state=tk.ACTIVE)
        self.load_progress["value"] = self.waitTime
        self.load_progress.update()
        vm_ip = vm.getInstaceIP()
        self.moodle_site = "http://" + vm_ip + "/moodle"
        self.php_my_admin_site = "http://" + vm_ip + "/phpmyadmin"
        self.ftp_site = "http://" + vm_ip + "/myftp"
        self.moo_button.config(state=tk.ACTIVE)
        self.php_button.config(state=tk.ACTIVE)
        self.ftp_button.config(state=tk.ACTIVE)

    def check_status(self):
        self.start_button.config(state=tk.DISABLED)
        self.start_button.update()
        vm.isInstanceReady()
        self.instanceIsReady = True
        self.set_ready()

    def display_progress(self):
        # Progress bar showing time elapsed to computer being up
        current_time = 0
        self.load_progress.place()
        self.load_progress['maximum'] = self.waitTime
        while self.instanceIsReady is False:
            current_time += 1
            self.load_progress["value"] = current_time
            self.load_progress.update()
            time.sleep(1)

    def start_check(self):
        check = Thread(target=self.check_status)
        display = Thread(target=self.display_progress)
        check.start()
        display.start()

    def log_out(self):
        vm.stopInstance()
        self.controller.show_frame("LoginPage")

    def open_page(self, url):
        webbrowser.open(url)


class TeacherPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Teacher Interface:", font=controller.title_font)
        label.grid(row=1, column=1, columnspan=2, pady=5, padx=10)
        self.config = gt.load_config()

        # Add AMI
        ami_label = tk.Label(self, text="AMI")
        ami_label.grid(row=2, column=1, sticky="W", padx=10)
        self.ami_entry = tk.Entry(self, width=20, font="none 12 bold", text=self.config["AMI"], highlightthickness=0)
        self.ami_entry.grid(row=3, column=1, padx=10, sticky='W')

        # Add Single Student Section
        add_label = tk.Label(self, text="Add Single Student", font="none 12 bold")
        add_label.grid(row=4, column=1, sticky="W", pady=10, padx=10)
        id_label = tk.Label(self, text="Student ID")
        id_label.grid(row=5, column=1, sticky='W', padx=10)
        em_label = tk.Label(self, text="Email")
        em_label.grid(row=5, column=2, sticky='W', padx=10)
        self.id_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.id_entry.grid(row=6, column=1, padx=10, sticky='W')
        self.em_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.em_entry.grid(row=6, column=2, padx=10, sticky='W')
        fn_label = tk.Label(self, text="First Name")
        fn_label.grid(row=7, column=1, sticky='W', padx=10)
        ln_label = tk.Label(self, text="Last Name")
        ln_label.grid(row=7, column=2, sticky='W', padx=10)
        self.fn_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.fn_entry.grid(row=8, column=1, padx=10)
        self.ln_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.ln_entry.grid(row=8, column=2, padx=10)

        # Add Student Via CSV
        add_mul_label = tk.Label(self, text="Add Multiple", font="none 12 bold")
        add_mul_label.grid(row=10, column=1, sticky="W", pady=10, padx=10)
        csv_label = tk.Label(self, text="File")
        csv_label.grid(row=11, column=1, sticky="W", padx=10)
        pro_label = tk.Label(self, text="Progress")
        pro_label.grid(row=11, column=2, sticky="W", padx=10)
        self.csv_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.csv_entry.insert(0, "Use open button.")
        self.csv_entry.grid(row=12, column=1, sticky="W", padx=10, pady=3)
        self.csv_progress = Progressbar(self, orient='horizontal', length=165, mode='determinate')
        self.csv_progress.grid(row=12, column=2, sticky="W", padx=10, pady=3)

        self.add_button = tk.Button(self, text="Add", command=lambda: self.add_one())
        self.add_button.grid(row=9, column=2, sticky="E", padx=10, pady=3)
        self.open_button = tk.Button(self, text="Open", command=lambda: self.open_file())
        self.open_button.grid(row=13, column=1, sticky="E", padx=10, pady=5)
        self.start_button = tk.Button(self, text="Start", command=lambda: self.create_multi_user())
        self.start_button.grid(row=13, column=2, sticky="E", padx=10, pady=5)

    def deactivate_buttons(self):
        self.add_button.config(state=tk.DISABLED)
        self.open_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)

    def activate_buttons(self):
        self.add_button.config(state=tk.ACTIVE)
        self.open_button.config(state=tk.ACTIVE)
        self.start_button.config(state=tk.ACTIVE)

    def open_file(self):
        temp_file = askopenfilename()
        if not temp_file.endswith(".csv"):
            messagebox.showinfo("File Type Error", "File type must be .csv")
        else:
            self.csv_entry.delete(0, 'end')
            self.csv_entry.insert(0, temp_file)

    def add_one(self):
        self.deactivate_buttons()
        temp_id = self.id_entry.get()
        e_mail = self.em_entry.get()
        first_name = self.fn_entry.get()
        last_name = self.ln_entry.get()
        ami = self.ami_entry.get()
        if temp_id != "" and e_mail != "" and first_name != "" and last_name != "" and ami != "":
            if gt.user_by_id(temp_id) is None:
                gt.create_single_user(temp_id, first_name, last_name, e_mail, ami)
            else:
                messagebox.showinfo("User Error", "This user already exist")
        else:
            messagebox.showinfo("Missing Requirements",
                                "ID, eMail, First Name, Last Name, and AMI fields must be filled.")
        self.config["AMI"] = ami
        gt.save_config(self.config)
        self.activate_buttons()

    def create_multi_user(self):
        ami = self.ami_entry.get()
        cs_file = self.csv_entry.get()
        self.deactivate_buttons()
        if cs_file != "" and ami != "":
            user_csv_list = []
            with open(cs_file, 'r', newline='') as CSV_FILE:
                reader = csv.reader(CSV_FILE)
                next(reader)
                for i in reader:
                    user_csv_list.append(i)

            # Sets up the progress bar
            self.csv_progress['maximum'] = len(user_csv_list)*2
            bar = 0

            # Creates user and assigns vm
            for new_user in user_csv_list:
                if not gt.user_by_id(int(new_user[0])):
                    gt.create_single_user(new_user[0], new_user[1], new_user[2], new_user[3], ami)
                bar += 1
                self.csv_progress["value"] = bar
                self.csv_progress.update()

            # waits for all machines to finish loading and shuts them down
            for curr_user in gt.get_list_users():
                if not curr_user.isTeacher:
                    curr_vm = gt.get_vm_object(curr_user.assigned_VM)
                    curr_vm.is_instance_ready()
                    curr_vm.stopInstance()
                    bar += 1
                self.csv_progress["value"] = bar
                self.csv_progress.update()

            messagebox.showinfo("Done", "Process completed.")
            self.csv_progress["value"] = 0
            self.csv_progress.update()
        else:
            messagebox.showinfo("Missing Info", "You need to first load a .csv file and provide a valid AMI.")
        self.config["AMI"] = ami
        gt.save_config(self.config)
        self.activate_buttons()


def shut_down():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        if vm:
            vm.stopInstance()
        app.destroy()


if __name__ == "__main__":
    app = EdEnvApp()
    app.protocol("WM_DELETE_WINDOW", shut_down)
    app.mainloop()
