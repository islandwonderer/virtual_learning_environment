import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from Sectioned_Version.UserManagementPage import UserManagementPage
from Sectioned_Version.TeacherPage import TeacherPage
from Sectioned_Version.StudentPage import StudentPage
from Sectioned_Version.LoginPage import LoginPage
from Sectioned_Version.GuestManagementPage import GuestManagementPage
from Sectioned_Version.VMManagementPage import VMManagementPage
from Sectioned_Version.SettingsPage import SettingsPage

user = None
vm = None


class EdEnvApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("IT Virtual Learning Environment")
        self.title_font = tkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, StudentPage, TeacherPage, UserManagementPage, GuestManagementPage, VMManagementPage,
                  SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        # self.show_frame("LoginPage")
        # self.show_frame("TeacherPage")
        # self.show_frame("StudentPage")
        self.show_frame("UserManagementPage")
        # self.show_frame("GuestManagementPage")
        # self.show_frame("VMManagementPage")
        # self.show_frame("SettingsPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def shut_down(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            if vm:
                vm.stopInstance()
            self.destroy()


if __name__ == "__main__":
    app = EdEnvApp()
    app.protocol("WM_DELETE_WINDOW", app.shut_down)
    app.mainloop()
