import tkinter as tk
import Gateway as gt
from tkinter import messagebox


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
            if user.isTeacher is False:
                if user.isSuspended is False:
                    vm = gt.get_vm_object(user.assigned_VM)
                    vm.startInstance()
                    self.controller.show_frame("StudentPage")
                else:
                    messagebox.showinfo("Warning", "Your Account Has Been Suspended. Please Contact Instructor", parent=self)
            else:
                self.controller.show_frame("TeacherPage")
        else:
            messagebox.showinfo("Warning", "Please Check Your Username And Password Then Try Again", parent=self)
