import customtkinter as ctk

class RemarkManager:
    def __init__(self, docker_tab, remark_frame):
        self.remark_frame = remark_frame
        # docker_tab should be the CTkTabview object from your main app
        self.docker_tab = docker_tab
        
        # Configure the command callback for the Tabview
        self.docker_tab.configure(command=self.on_tab_changed)
        
        self.setup_ui()

    def setup_ui(self):
        # ... (Your existing UI setup code)
        # Note: Be careful with 'self.remark_frame' naming, 
        # you are overwriting the reference passed in __init__
        self.container_frame = ctk.CTkFrame(self.remark_frame, width=400)
        self.container_frame.grid(row=0, column=7, columnspan=2, rowspan=2, sticky='nsew')

        self.remark_tabview = ctk.CTkTabview(self.container_frame, width=400, height=500)
        self.remark_tabview.pack(fill='both', expand=True)
        self.remark_tabview.add('Remarks')
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.remark_tabview.tab('Remarks'), height=750, width=380)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")

        self.remark = ctk.CTkTextbox(
            self.scroll_frame, 
            font=("Comic Sans MS", 25),
            width=400,
            height=700,
            fg_color=["#C0C8CE", "#2B2D2F"],
        )
        self.remark.grid(row=2, column=0, sticky="nsew")

    def on_tab_changed(self):
        # CTkTabview.get() returns the name of the currently selected tab
        current_tab_name = self.docker_tab.get()
        print(f"Tab changed to: {current_tab_name}")

        # Clear existing text before inserting new info
        self.remark.delete("0.0", "end")
        
        if current_tab_name == "Containers":
            msg = "Viewing Docker Containers list..."
        elif current_tab_name == "Images":
            msg = "Viewing downloaded Docker Images..."
        else:
            msg = f"Welcome to {current_tab_name}!"

        self.remark.insert("0.0", f"{msg}\nInfo remark updated.")