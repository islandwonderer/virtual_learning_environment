# Imported Libraries
import tkinter as tk
import webbrowser
from tkinter import messagebox
import datetime
from botocore.exceptions import WaiterError

# Local Imports
from controller_and_modules import Controller as cT


class GuestManagementPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.users = self.get_valid_users()
        self.curr_user = None
        self.is_toggled = False
        self.has_list = True
        self.disconnect_flag = False

        # Label and Nav
        top_label = tk.Label(self, text="Guest Access:", font=controller.title_font)
        top_label.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
        self.bk_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StudentPage"))
        self.bk_button.grid(row=1, column=2, padx=10, sticky=tk.E)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # Search Section
        ser_label = tk.Label(self, text="Find (First Name or Last Name)")
        ser_label.grid(row=2, column=1, pady=3, padx=10, sticky=tk.W)
        self.ser_entry = tk.Entry(self, width=37, font="none 12 bold", highlightthickness=0)
        self.ser_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=10, pady=3)
        self.ser_button = tk.Button(self, text="Search", command=self.search)
        self.ser_button.grid(row=3, column=2, sticky=tk.E, padx=10, pady=3)

        # List of Users
        self.user_list = tk.Listbox(self, height=13, width=48)
        self.user_list.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W, rowspan=15, columnspan=2)
        self.update_list()
        self.user_list.bind('<<ListboxSelect>>', self.on_select)

        # Connect Button
        self.link_button = tk.Button(self, text="Goto Page", command=lambda: self.connect(),
                                     state=tk.DISABLED)
        self.link_button.grid(row=23, column=2, sticky=tk.E, padx=10, pady=3)

    def update_list(self):
        self.user_list.delete(0, tk.END)
        self.users = cT.get_list_users()
        for user in self.users:
            if user.isTeacher is not None:
                text = "{}, {}"
                text = text.format(user.lastName, user.firstName)
                self.user_list.insert(tk.END, text)
        self.user_list.update()

    def on_select(self, event):
        widget = event.widget
        index = widget.curselection()[0]
        self.curr_user = self.users[index]

        # Sets the VM globally in case of shutdown of app
        self.controller.vm = cT.get_vm_object(self.curr_user.assigned_VM)
        self.link_button.config(state=tk.ACTIVE)
        self.link_button.update()

    def connect(self):
        self.disconnect_flag = False
        self.user_list.config(state=tk.DISABLED)
        self.ser_button.config(state=tk.DISABLED)
        self.link_button.config(state=tk.DISABLED)
        self.user_list.update()
        self.ser_button.update()
        self.link_button.update()
        self.toggle_button()
        curr_vm = self.controller.vm
        curr_vm.start_instance()
        messagebox.showinfo("Warning",
                            "This process may take while. A window will open on your browser when its ready.",
                            parent=self)
        try:
            curr_vm.is_instance_ready()
            site = "http://" + curr_vm.get_instance_ip() + "/moodle"
            webbrowser.open(site)
            self.log_visit()
            self.link_button.config(state=tk.ACTIVE)
            self.link_button.update()

        except WaiterError:
            messagebox.showinfo("Warning",
                                "There was a problem connecting to the remote computer. Please log out and try again"
                                "in 5 minutes.", parent=self)
            self.disconnect()

    def disconnect(self):
        curr_vm = self.controller.vm
        curr_vm.stop_instance()
        self.disconnect_flag = True

        # Returns Global VM to Users
        self.controller.vm = cT.get_vm_object(self.controller.user.assigned_VM)

        self.toggle_button()
        self.user_list.config(state=tk.NORMAL)
        self.ser_button.config(state=tk.ACTIVE)
        self.user_list.update()
        self.ser_button.update()

    def toggle_button(self):
        if self.is_toggled is False:
            self.is_toggled = True
            self.link_button.config(text="Disconnect", command=lambda: self.disconnect())
            self.link_button.update()
        else:
            self.is_toggled = False
            self.link_button.config(text="Connect", command=lambda: self.connect())
            self.link_button.update()

    def log_visit(self):
        user = self.controller.user
        date_stamp = datetime.datetime.now()
        date_stamp = date_stamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        self.curr_user.add_to_log(date_stamp, (user.firstName + user.lastName))
        cT.save_user(self.curr_user)
        subject = "Notification of VM Access"
        message = "{},\n The following is to notify you that {} {} accessed your VM on {}. " \
                  "If something has changed in" \
                  "your configuration notify " \
                  "an instructor at your earliest continence.".format(self.curr_user.firstName, user.firstName,
                                                                      user.lastName, date_stamp)
        cT.notify_user(self.curr_user, subject, message)

    def search(self):
        term = self.ser_entry.get()
        counter = 0
        if term == "":
            self.update_list()
            self.link_button.config(state=tk.DISABLED)
        else:
            if " " in term:
                messagebox.showinfo("Warning", "Please enter a single search term", parent=self)
            else:
                self.user_list.delete(0, tk.END)
                for ser_user in self.users:
                    if term in ser_user.lastName or term in ser_user.firstName:
                        text = "{}, {}"
                        text = text.format(ser_user.lastName, ser_user.firstName)
                        self.user_list.insert(tk.END, text)
                        self.user_list.update()
                        counter += 1
                if counter is 0:
                    messagebox.showinfo("Warning", "No matching records.", parent=self)
                    self.update_list()

    @staticmethod
    def get_valid_users():
        valid_users = []
        all_users = cT.get_list_users()
        for user in all_users:
            if user.assigned_VM is not None:
                valid_users.append(user)
        return valid_users
