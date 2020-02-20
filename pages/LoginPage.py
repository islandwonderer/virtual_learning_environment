# Imported Packages
import tkinter as tk
from tkinter import messagebox

# Local Imports
from controller_and_modules import Controller as cT


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
        self.has_list = False

    def verify_login(self):
        user_id = int(self.unEntry.get())
        if cT.verify_user(user_id, self.pwEntry.get()):
            user = cT.user_by_id(user_id)
            if user.isTeacher is False:
                if user.isSuspended is False:
                    self.controller.vm = cT.get_vm_object(user.assigned_VM)
                    self.controller.vm.start_instance()
                    self.controller.user = user
                    self.controller.show_frame("StudentPage")
                else:
                    messagebox.showinfo("Warning", "Your Account Has Been Suspended. Please Contact Instructor",
                                        parent=self)
            else:
                self.controller.show_frame("TeacherPage")
        else:
            messagebox.showinfo("Warning", "Please Check Your Username And Password Then Try Again", parent=self)
