import tkinter as tk
import Gateway as gt
import webbrowser
from tkinter import messagebox


class UserManagementPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        top_label = tk.Label(self, text="User Management:", font=controller.title_font)
        top_label.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

        # Users List
        users_label = tk.Label(self, text="Users")
        users_label.grid(row=2, column=1, padx=10, sticky=tk.W)
        self.bk_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("TeacherPage"))
        self.bk_button.grid(row=1, column=2, padx=10, sticky=tk.E)
        self.user_list = tk.Listbox(self, height=18)
        self.user_list.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W, rowspan=20)
        self.users = self.update_list()
        self.user_list.bind('<<ListboxSelect>>', self.on_select)

        # Selected User Details
        id_label = tk.Label(self, text="Student ID")
        id_label.grid(row=2, column=2, padx=10, sticky=tk.W)
        self.id_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.id_entry.grid(row=3, column=2, padx=10)
        first_label = tk.Label(self, text="First Name")
        first_label.grid(row=4, column=2, padx=10, sticky=tk.W)
        self.fn_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.fn_entry.grid(row=5, column=2, padx=10)
        last_label = tk.Label(self, text="Last Name")
        last_label.grid(row=6, column=2, padx=10, sticky=tk.W)
        self.ln_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.ln_entry.grid(row=7, column=2, padx=10)
        email_label = tk.Label(self, text="eMail")
        email_label.grid(row=8, column=2, padx=10, sticky=tk.W)
        self.email_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.email_entry.grid(row=9, column=2, padx=10)
        pass_label = tk.Label(self, text="Password")
        pass_label.grid(row=10, column=2, padx=10, sticky=tk.W)
        self.pass_entry = tk.Entry(self, width=20, font="none 12 bold", highlightthickness=0)
        self.pass_entry.grid(row=11, column=2, padx=10)
        suspend_label = tk.Label(self, text="Suspended")
        suspend_label.grid(row=12, column=2, padx=10, sticky=tk.W)
        suspend_frame = tk.Frame(self)
        suspend_frame.grid(row=13, column=2, sticky=tk.NSEW, padx=10)
        self.suspended = False
        self.yes_button = tk.Button(suspend_frame, command=lambda: self.toggle_suspend(),
                                    text="Yes", state=(tk.ACTIVE if self.suspended is False else tk.DISABLED),
                                    highlightbackground="#ffffff")
        self.no_button = tk.Button(suspend_frame, command=lambda: self.toggle_suspend(),
                                   text="No", state=(tk.DISABLED if self.suspended is False else tk.ACTIVE),
                                   highlightbackground="#ffffff")
        self.no_button.pack(side=tk.RIGHT)
        self.yes_button.pack(side=tk.RIGHT)
        self.web_site = tk.Label(self, text="Click Here To Visit Student Site", fg="blue", cursor="hand2")
        self.web_site.grid(row=14, column=2, sticky=tk.NSEW, padx=10, pady=10)
        self.web_site.bind("<Button-1>", lambda e: self.open_site())
        user_opt_frame = tk.Frame(self)
        user_opt_frame.grid(row=15, column=2, sticky=tk.NSEW, padx=10)
        self.upd_button = tk.Button(user_opt_frame, text="Update", command=lambda: self.update_user())
        self.del_button = tk.Button(user_opt_frame, text="Delete", command=lambda: self.delete_user())
        self.upd_button.pack(side=tk.RIGHT)
        self.del_button.pack(side=tk.RIGHT)

    def toggle_suspend(self):
        if self.suspended is False:
            self.suspended = True
            self.yes_button.config(state=tk.ACTIVE)
            self.no_button.config(state=tk.DISABLED)
            self.yes_button.update()
            self.no_button.update()
        else:
            self.suspended = False
            self.yes_button.config(state=tk.DISABLED)
            self.no_button.config(state=tk.ACTIVE)
            self.yes_button.update()
            self.no_button.update()

    def on_select(self, event):
        widget = event.widget
        index = widget.curselection()[0]
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, self.users[index].studentID)
        self.fn_entry.delete(0, tk.END)
        self.fn_entry.insert(0, self.users[index].firstName)
        self.ln_entry.delete(0, tk.END)
        self.ln_entry.insert(0, self.users[index].lastName)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, self.users[index].eMail)
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, self.users[index].password)
        self.suspended = self.users[index].isSuspended

    def open_site(self):
        global vm
        messagebox.showinfo("Warning", "This process may take while. A window will open on your browser when its ready.")
        index = self.user_list.curselection()
        curr_user = self.users[index[0]]
        if curr_user.assignedVM is not None:
            vm = gt.get_vm_object(curr_user.assignedVM)
            vm.startInstance()
            vm.isInstanceReady()
            site = "http://" + vm.getInstaceIP() + "/moodle"
            webbrowser.open(site)
        else:
            messagebox.showinfo("Warning", "This is a teacher and does not have VM assigned.")

    def update_user(self):
        index = self.user_list.curselection()
        curr_user = self.users[index[0]]
        curr_user.studentID = self.id_entry.get()
        curr_user.setAutoUsername()
        curr_user.firstName = self.fn_entry.get()
        curr_user.lastName = self.ln_entry.get()
        curr_user.eMail = self.email_entry.get()
        curr_user.password = self.pass_entry.get()
        curr_user.isSuspended = self.suspended
        gt.save_user(curr_user)
        messagebox.showinfo("Update", "The user information has been updated.")

    def delete_user(self):
        index = self.user_list.curselection()[0]
        print("print index is", index)
        curr_user = self.users[index]
        if curr_user.isTeacher is False:
            curr_vm = gt.get_vm_object(curr_user.assigned_VM)
            user_response = messagebox.askokcancel("Delete", "Are you sure you want to delete this user? "
                                                           "This will result in the irreversible deletion of the "
                                                           "associated VM.", parent=self)
            if user_response is False:
                print("Canceled")

            else:
                # delete current user VM
                gt.del_vm(curr_vm)
                # delete current user
                gt.del_user(curr_user)
                # refresh the list of students
                self.update_list()

        else:
            messagebox.showinfo("Warning", "This is a teacher and cannot be removed this way.")

    def update_list(self):
        self.user_list.delete(0, tk.END)
        users = gt.get_list_users()
        for user in users:
            text = "{}, {}, {}"
            text = text.format(user.lastName, user.firstName, user.studentID)
            self.user_list.insert(tk.END, text)
        self.user_list.update()
        return users



