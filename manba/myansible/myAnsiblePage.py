import threading
import customtkinter as ctk
import subprocess

from myansible.frames.ansibleMainFrame import AnsibleMainFrame
from myansible.setupSSH.containerSSH import SetupAnsible, UpdateTextbox, ProgressBar


class MyAnsiblePage( ctk.CTkFrame ) :
    def __init__( self, master ) :
        super( ).__init__( master )
# Setup GUI
        self.main_frame = AnsibleMainFrame( master )
        self.main_frame.ansible_frame( )

# Setup logging
        from myansible.setupSSH.containerSSH import ProgressBar
        self.progressbar_helper = ProgressBar( self.main_frame.progressbar )
        self.updateTextbox = UpdateTextbox( self.main_frame.ansible_textbox )

# Progressbar
        self.progressbar = ProgressBar( self.main_frame.progressbar )

# Intagrate Functions
        self.setupAnsible = SetupAnsible( logger = self.updateTextbox, progressbar = self.progressbar_helper )

# Combine Anisible and Functions
        self.main_frame.inventory_tab.try_ping_btn.configure( command = self.start_setup_thread )

    # def setup_ansible( self ) :
    #     container_list = self.main_frame.inventory_tab.selected_container()
    #     install_list = list()
    #     for i in container_list :
    #         install_list.append( str( i[3] ) )
    #         if i[2] != "running" :
    #             run_container = subprocess.run(
    #                 [ 'docker', 'start', str( i[3] ) ],
    #                 capture_output = True,
    #                 text = True
    #             )
        # print( install_list )
        # print( container_list )
        
        # self.setupAnsible.setup_ansible( container_names = install_list )
        # container_list = self.main_frame.inventory_tab.refrest_container_list( )

    def start_setup_thread( self ) :
        self.main_frame.progressbar.configure(mode="indeterminate")
        thread = threading.Thread( target = self.setup_ansible )
        thread.daemon = True
        thread.start( )
    
    def setup_ansible( self ) :
        container_list = self.main_frame.inventory_tab.selected_container()
        install_list = [str(i[3]) for i in container_list]
        self.progressbar_helper.start_loading()
        for i in container_list:
            if i[2] != "running":
                subprocess.run(['docker', 'start', str(i[3])], capture_output=True, text=True)
        
        self.setupAnsible.setup_ansible(container_names=install_list)
        self.main_frame.inventory_tab.refrest_container_list()
        self.progressbar_helper.stop_loading()