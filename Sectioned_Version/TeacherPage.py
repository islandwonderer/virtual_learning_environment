import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import csv
import Gateway as gt
from tkinter import messagebox


class TeacherPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Teacher Interface:", font=controller.title_font)
        label.grid(row=1, column=1, pady=3, padx=10, sticky=tk.W)
        self.config = gt.load_config()
        self.has_list = False

        # Management Buttons
        man_label = tk.Label(self, text="Manage", font="none 12 bold")
        man_label.grid(row=2, column=1, sticky=tk.W, padx=10)
        manage_buttons = tk.Frame(self)
        manage_buttons.grid(row=3, column=1, sticky=tk.EW, padx=10)
        self.users_button = tk.Button(manage_buttons, text="Users",
                                      command=lambda: self.controller.show_frame("UserManagementPage"))
        self.VM_button = tk.Button(manage_buttons, text="VMs",
                                   command=lambda: self.controller.show_frame("VMManagementPage"))
        self.settings_button = tk.Button(manage_buttons, text="Settings",
                                        command=lambda: self.controller.show_frame("SettingsPage"))
        self.VM_button.pack(side=tk.LEFT)
        self.users_button.pack(side=tk.LEFT)
        self.settings_button.pack(side=tk.LEFT)

        # Add Single Student Section
        add_label = tk.Label(self, text="Add Single Student", font="none 12 bold")
        add_label.grid(row=4, column=1, sticky=tk.W, pady=10, padx=10)
        id_label = tk.Label(self, text="Student ID")
        id_label.grid(row=5, column=1, sticky=tk.W, padx=10)
        em_label = tk.Label(self, text="Email")
        em_label.grid(row=5, column=2, sticky=tk.W, padx=10)
        self.id_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.id_entry.grid(row=6, column=1, padx=10, sticky=tk.W)
        self.em_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.em_entry.grid(row=6, column=2, padx=10, sticky=tk.W)
        fn_label = tk.Label(self, text="First Name")
        fn_label.grid(row=7, column=1, sticky=tk.W, padx=10)
        ln_label = tk.Label(self, text="Last Name")
        ln_label.grid(row=7, column=2, sticky=tk.W, padx=10)
        self.fn_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.fn_entry.grid(row=8, column=1, padx=10, sticky=tk.W)
        self.ln_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.ln_entry.grid(row=8, column=2, padx=10, sticky=tk.W)

        # Add Student Via CSV
        add_mul_label = tk.Label(self, text="Add Multiple", font="none 12 bold")
        add_mul_label.grid(row=10, column=1, sticky=tk.W, pady=10, padx=10)
        csv_label = tk.Label(self, text="File")
        csv_label.grid(row=11, column=1, sticky=tk.W, padx=10)
        pro_label = tk.Label(self, text="Progress")
        pro_label.grid(row=11, column=2, sticky=tk.W, padx=10)
        self.csv_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.csv_entry.insert(0, "Use open button.")
        self.csv_entry.grid(row=12, column=1, sticky=tk.W, padx=10, pady=3)
        self.csv_progress = Progressbar(self, orient='horizontal', length=165, mode='determinate')
        self.csv_progress.grid(row=12, column=2, sticky=tk.W, padx=10, pady=3)
        self.add_button = tk.Button(self, text="Add", command=lambda: self.add_one_user())
        self.add_button.grid(row=9, column=2, sticky="E", padx=10, pady=3)
        self.open_button = tk.Button(self, text="Open", command=lambda: self.open_file())
        self.open_button.grid(row=13, column=1, sticky="E", padx=10, pady=5)
        self.start_button = tk.Button(self, text="Start", command=lambda: self.create_multi_user())
        self.start_button.grid(row=13, column=2, sticky="E", padx=10, pady=5)

        # List of buttons for enabling and disabling
        self.buttons_list = [self.add_button, self.open_button, self.start_button, self.users_button, self.VM_button,
                             self.settings_button]

    def deactivate_buttons(self):
        for button in self.buttons_list:
            button.config(state=tk.DISABLED)
            button.update()

    def activate_buttons(self):
        for button in self.buttons_list:
            button.config(state=tk.ACTIVE)
            button.update()

    def clear_single_user_fields(self):
        self.id_entry.delete(0, tk.END)
        self.ln_entry.delete(0, tk.END)
        self.fn_entry.delete(0, tk.END)
        self.em_entry.delete(0, tk.END)

    def clear_multi_user_fields(self):
        self.csv_entry.delete(0, tk.END)

    def open_file(self):
        temp_file = askopenfilename()
        if not temp_file.endswith(".csv"):
            messagebox.showinfo("File Type Error", "File type must be .csv", parent=self)
        else:
            self.csv_entry.delete(0, 'end')
            self.csv_entry.insert(0, temp_file)

    def add_one_user(self):
        self.deactivate_buttons()
        temp_id = int(self.id_entry.get())
        e_mail = self.em_entry.get()
        first_name = self.fn_entry.get()
        last_name = self.ln_entry.get()
        # Checks that all the fields are filled in.
        if temp_id != "" and e_mail != "" and first_name != "" and last_name != "":
            # Checks that user has not been previously added
            if gt.user_by_id(temp_id) is None:
                curr_user = gt.create_single_user(temp_id, first_name, last_name, e_mail)[0]
                curr_vm = gt.get_vm_object(curr_user.assigned_VM)
                curr_vm.is_instance_ready()
                curr_vm.stop_instance()
            else:
                messagebox.showinfo("User Error", "This user already exist", parent=self)
        else:
            messagebox.showinfo("Missing Requirements",
                                "ID, eMail, First Name, and Last Name fields must be filled.", parent=self)
        self.clear_single_user_fields()
        self.activate_buttons()

    def create_multi_user(self):
        cs_file = self.csv_entry.get()
        self.deactivate_buttons()
        if cs_file != "":
            user_csv_list = []
            with open(cs_file, 'r', newline='') as CSV_FILE:
                reader = csv.reader(CSV_FILE)
                next(reader)
                for user_list in reader:
                    user_csv_list.append(user_list)
            # Sets up the progress bar
            self.csv_progress['maximum'] = len(user_csv_list)*2
            bar = 0

            # Creates user and assigns vm
            for new_user in user_csv_list:
                if new_user:
                    if gt.user_by_id(int(new_user[0])) is None:
                        success = gt.create_single_user(new_user[0].strip(), new_user[1].strip(), new_user[2].strip(), new_user[3].strip())
                        if not success[1]:
                            messagebox.showinfo("Warning", "Unable to notify user {0} of their account's password.".format(new_user[0]), parent=self)
                bar += 1
                self.csv_progress["value"] = bar
                self.csv_progress.update()

            # waits for all machines to finish loading and shuts them down
            for curr_user in gt.get_list_users():
                if curr_user.isTeacher is False:
                    curr_vm = gt.get_vm_object(curr_user.assigned_VM)
                    curr_vm.is_instance_ready()
                    curr_vm.stop_instance()
                    bar += 1
                self.csv_progress["value"] = bar
                self.csv_progress.update()

            messagebox.showinfo("Done", "Process completed.", parent=self)
            self.csv_progress["value"] = 0
            self.csv_progress.update()
        else:
            messagebox.showinfo("Missing Info", "You need to first load a .csv file and provide a valid AMI.", parent=self)
        self.clear_multi_user_fields()
        self.activate_buttons()
