import tkinter as tk
import Gateway as gt
import json
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox


class VMManagementPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        top_label = tk.Label(self, text="VM Management:", font=controller.title_font)
        top_label.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
        self.bk_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("TeacherPage"))
        self.bk_button.grid(row=1, column=2, padx=10, sticky=tk.E)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.user_list = self.get_valid_users()

        # Power Management
        power_label = tk.Label(self, text="Power", font="none 12 bold")
        power_label.grid(row=2, column=1, padx=10, sticky=tk.W)
        cont_frame = tk.Frame(self)
        cont_frame.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=10)
        self.pwrall_button = tk.Button(cont_frame, text="Power All", command=lambda: self.power_all())
        self.shtall_button = tk.Button(cont_frame, text="Shutdown All", command=lambda: self.shutdown_all())
        self.pwrall_button.pack(side=tk.LEFT)
        self.shtall_button.pack(side=tk.LEFT)

        # VM List
        vm_label = tk.Label(self, text="VMs", font="none 12 bold")
        vm_label.grid(row=4, column=1, padx=10, sticky=tk.W)
        self.vm_list = tk.Listbox(self, height=15)
        self.vm_list.grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW, rowspan=20)
        self.update_list()
        self.vm_list.bind('<<ListboxSelect>>', self.on_select)

        # VM Info
        info_label = tk.Label(self, text="Info", font="none 12 bold")
        info_label.grid(row=4, column=2, padx=10, sticky=tk.W)
        ami_info = tk.Label(self, text="AMI", font="none 12 underline")
        ami_info.grid(row=5, column=2, padx=10, sticky=tk.W)
        self.ami_out = tk.Label(self, text="None")
        self.ami_out.grid(row=6, column=2, padx=10, pady=2, sticky=tk.W)
        owner_info = tk.Label(self, text="Owner", font="none 12 underline")
        owner_info.grid(row=7, column=2, padx=10, sticky=tk.W)
        self.owner_out = tk.Label(self, text="None")
        self.owner_out.grid(row=8, column=2, padx=10, pady=2, sticky=tk.W)
        status_info = tk.Label(self, text="Status", font="none 12 underline")
        status_info.grid(row=9, column=2, padx=10, sticky=tk.W)
        self.status_out = tk.Label(self, text="None")
        self.status_out.grid(row=10, column=2, padx=10, pady=2, sticky=tk.W)
        dwn_info = tk.Label(self, text="Visitors Logs", font="none 12 underline")
        dwn_info.grid(row=11, column=2, padx=10, sticky=tk.W)
        self.dwn_button = tk.Button(self, text="Download", state=tk.DISABLED)
        self.dwn_button.grid(row=12, column=2, padx=10, sticky=tk.EW)

    def on_select(self, event):
        widget = event.widget
        index = widget.curselection()[0]
        print(self.user_list[index])
        vm = gt.get_vm_object(self.user_list[index].assigned_VM)
        print(vm)
        info = vm.getInfo()
        self.ami_out.config(text=info['Reservations'][0]['Instances'][0]['ImageId'])
        self.owner_out.config(text=(self.user_list[index].firstName + " " + self.user_list[index].lastName))
        self.status_out.config(text=info['Reservations'][0]['Instances'][0]['State']['Name'])
        self.dwn_button.config(state=tk.ACTIVE, command=lambda: self.download(vm))

    def power_all(self):
        for vm_user in self.user_list:
            if vm_user.assigned_VM is not None:
                curr_vm = gt.get_vm_object(vm_user.assigned_VM)
                curr_vm.startInstance()
                print(curr_vm)

    def shutdown_all(self):
        for vm_user in self.user_list:
            if vm_user.assigned_VM is not None:
                curr_vm = gt.get_vm_object(vm_user.assigned_VM)
                curr_vm.stopInstance()

    def update_list(self):
        for vm_user in self.user_list:
            if vm_user.assigned_VM is not None:
                self.vm_list.insert(tk.END, vm_user.assigned_VM)

    def download(self, vm):
        file = asksaveasfilename(initialdir="/", title="Save File", filetypes={("JSON files", "*.json")})
        log = vm.getLog()
        try:
            if file.endswith(".json"):
                with open(file, 'w') as json_file:
                    json.dump(log, json_file)
            else:
                file_name = file + ".json"
                with open(file_name, 'w') as json_file:
                    json.dump(log, json_file)
        except OSError:
            messagebox.showinfo("Error", "Read only filesystem. \n Save at alternative location.", parent=self)

    def get_valid_users(self):
        valid_users = []
        all_users = gt.get_list_users()
        for user in all_users:
            if user.assigned_VM is not None:
                valid_users.append(user)
        return valid_users
