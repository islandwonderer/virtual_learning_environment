import tkinter as tk
from tkinter.ttk import *
import Gateway as gt
from tkinter import messagebox
import webbrowser
from threading import Thread
import time


class StudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        stat_label = tk.Label(self, text="Student Interface:", font=controller.title_font)
        stat_label.grid(row=1, column=1, pady=5, padx=10, sticky=tk.NSEW)
        self.has_list = False

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
        self.moo_button.grid(row=6, column=1, pady=12)
        self.moo_info = tk.Message(self, text=self.config['mood_info'], width=165, font=(None, 10))
        self.moo_info.grid(row=6, column=2, sticky=tk.W)
        self.php_button = tk.Button(self, text="phpAdmin", command=lambda: self.open_page(self.php_my_admin_site), state=tk.DISABLED)
        self.php_button.grid(row=7, column=1, pady=12)
        self.php_info = tk.Message(self, text=self.config['php_info'], width=165, font=(None, 10))
        self.php_info.grid(row=7, column=2, sticky=tk.W)
        self.ftp_button = tk.Button(self, text="FTP", command=lambda: self.open_page(self.ftp_site),  state=tk.DISABLED)
        self.ftp_button.grid(row=8, column=1, pady=12)
        self.ftp_info = tk.Message(self, text=self.config['ftp_info'], width=165, font=(None, 10))
        self.ftp_info.grid(row=8, column=2, sticky=tk.W)

        # Section Separation
        separator_line2 = Separator(self, orient="horizontal")
        separator_line2.grid(row=9, column=1, columnspan=2, padx=15, pady=20, sticky="EW")

        # Guest Visit Section
        vis_label = tk.Label(self, text="Other Class VMs")
        vis_label.grid(row=10, column=2, sticky="W", padx=10, pady=12)
        self.vis_button = tk.Button(self, text="Visit", command=lambda: self.controller.show_frame("GuestManagementPage"))
        self.vis_button.grid(row=10, column=2, sticky="E", padx=10, pady=12)

    def set_ready(self):
        messagebox.showinfo("Ready", "Your instance is ready!", parent=self)
        self.start_button.config(text="LogOut", command=lambda: self.log_out())
        self.start_button.config(state=tk.ACTIVE)
        self.load_progress["value"] = self.waitTime
        self.load_progress.update()
        vm_ip = self.controller.vm.getInstaceIP()
        self.moodle_site = "http://" + vm_ip + "/moodle"
        self.php_my_admin_site = "http://" + vm_ip + "/phpmyadmin"
        self.ftp_site = "http://" + vm_ip + "/myftp"
        self.moo_button.config(state=tk.ACTIVE)
        self.php_button.config(state=tk.ACTIVE)
        self.ftp_button.config(state=tk.ACTIVE)

    def check_status(self):
        vm = self.controller.vm
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
        self.controller.vm.stopInstance()
        self.controller.show_frame("LoginPage")

    @staticmethod
    def open_page(url):
        webbrowser.open(url)

