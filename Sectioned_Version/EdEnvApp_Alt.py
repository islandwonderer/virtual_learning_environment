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


class EdEnvApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("IT Virtual Learning Environment")
        self.title_font = tkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.vm = None
        self.user = None

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

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        # Select frame
        frame = self.frames[page_name]
        # Refresh the list if it has a list.
        if frame.has_list is True:
            frame.update_list()
        # Display Frame
        frame.tkraise()

    def shut_down(self):
        # Prevents VM's to remain running when user exits
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?", parent=self):
            if self.vm:
                self.vm.stop_instance()
            self.destroy()


if __name__ == "__main__":
    app = EdEnvApp()
    app.protocol("WM_DELETE_WINDOW", app.shut_down)
    app.mainloop()
