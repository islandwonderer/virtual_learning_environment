# Imported Packages
import tkinter as tk
from tkinter import messagebox

# Local Imports
from controller_and_modules import Controller as cT


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings:", font=controller.title_font)
        label.grid(row=1, column=1, pady=3, padx=10, sticky=tk.W)
        self.config = cT.load_config()
        self.has_list = False

        # VM Settings
        vm_settings_label = tk.Label(self, text="VM Settings", font="none 12 bold")
        vm_settings_label.grid(row=2, column=1, sticky=tk.W, padx=10)

        # Add AMI
        ami_label = tk.Label(self, text="AMI")
        ami_label.grid(row=3, column=1, sticky=tk.W, padx=10)
        self.ami_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.ami_entry.grid(row=4, column=1, padx=10, sticky=tk.W)

        # Add VM Type
        vm_type_label = tk.Label(self, text="VM Type")
        vm_type_label.grid(row=3, column=2, sticky=tk.W, padx=10)
        self.vm_type_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.vm_type_entry.grid(row=4, column=2, padx=10, sticky=tk.W)

        # Add Key Name
        key_label = tk.Label(self, text="Key Name")
        key_label.grid(row=5, column=1, sticky=tk.W, padx=10)
        self.key_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.key_entry.grid(row=6, column=1, padx=10, sticky=tk.W)

        # Add Security Group
        group_label = tk.Label(self, text="Security Group")
        group_label.grid(row=5, column=2, sticky=tk.W, padx=10)
        self.group_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.group_entry.grid(row=6, column=2, padx=10, sticky=tk.W)

        # Email Settings
        email_settings_label = tk.Label(self, text="eMail Settings", font="none 12 bold")
        email_settings_label.grid(row=7, column=1, sticky=tk.W, padx=10, pady=5)

        # Add Email Address
        email_label = tk.Label(self, text="eMail")
        email_label.grid(row=8, column=2, sticky=tk.W, padx=10)
        self.email_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.email_entry.grid(row=9, column=2, padx=10, sticky=tk.W)

        # Add Password
        password_label = tk.Label(self, text="Password")
        password_label.grid(row=8, column=1, sticky=tk.W, padx=10)
        self.password_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.password_entry.grid(row=9, column=1, padx=10, sticky=tk.W)

        # Add sMTP
        smtp_label = tk.Label(self, text="SMTP")
        smtp_label.grid(row=10, column=1, sticky=tk.W, padx=10)
        self.smtp_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.smtp_entry.grid(row=11, column=1, padx=10, sticky=tk.W)

        # Add Port
        port_label = tk.Label(self, text="Port")
        port_label.grid(row=10, column=2, sticky=tk.W, padx=10)
        self.port_entry = tk.Entry(self, width=22, font="none 12 bold", highlightthickness=0)
        self.port_entry.grid(row=11, column=2, padx=10, sticky=tk.W)

        # Save and Cancel Button
        settings_buttons = tk.Frame(self)
        settings_buttons.grid(row=12, column=2, sticky=tk.E, padx=10, pady=10)
        self.save_button = tk.Button(settings_buttons, text="Save", command=lambda: self.save_settings())
        self.cancel_button = tk.Button(settings_buttons, text="Cancel", command=lambda: self.cancel_warning())
        self.save_button.pack(side=tk.LEFT)
        self.cancel_button.pack(side=tk.LEFT)

        # Loads Current Settings
        self.load_settings()

    def save_settings(self):
        self.config["AMI"] = self.ami_entry.get()
        self.config["instance_type"] = self.vm_type_entry.get()
        self.config["key_name"] = self.key_entry.get()
        self.config["security_group_id"] = self.group_entry.get()
        self.config["email"] = self.email_entry.get()
        self.config["e_password"] = self.password_entry.get()
        self.config["smtp"] = self.smtp_entry.get()
        self.config["port"] = int(self.port_entry.get())
        cT.save_config(self.config)
        self.controller.show_frame("TeacherPage")

    def load_settings(self):
        self.ami_entry.insert(0, self.config["AMI"])
        self.vm_type_entry.insert(0, self.config["instance_type"])
        self.key_entry.insert(0, self.config["key_name"])
        self.group_entry.insert(0, self.config["security_group_id"])
        self.email_entry.insert(0, self.config["email"])
        self.password_entry.insert(0, self.config["e_password"])
        self.smtp_entry.insert(0, self.config["smtp"])
        self.port_entry.insert(0, self.config["port"])

    def cancel_warning(self):
        result = messagebox.askokcancel("Warning",
                                        "Do you want to continue? Any changes to these settings will be lost.",
                                        parent=self)
        if result is True:
            self.controller.show_frame("TeacherPage")
        else:
            return


