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

        self.main_frame.inventory_tab.try_ping_btn.configure( command = self.run_ansible_ping)
        self.main_frame.inventory_tab.setup_btn.configure( command = self.start_setup_thread )
        self.main_frame.inventory_tab.run_btn.configure( command = self.run_playbook )
        self.main_frame.inventory_tab.clean_btn.configure( command = self.updateTextbox.clear_textbox )

    def start_setup_thread( self ) :
        self.main_frame.progressbar.configure(mode="indeterminate")
        thread = threading.Thread( target = self.setup_ansible )
        thread.daemon = True
        thread.start( )


    def setup_ansible( self ) :
        container_list = self.main_frame.inventory_tab.selected_container()
        install_list = [str(i[2]) for i in container_list]
        self.progressbar_helper.start_loading()
        for i in container_list:
            if i[2] != "running":
                subprocess.run(['docker', 'start', str(i[2])], capture_output=True, text=True)
        
        self.setupAnsible.setup_ansible(container_names=install_list)
        self.progressbar_helper.stop_loading()
    
    def run_ansible_ping( self ):
        """Executes ansible all -m ping and displays output in the textbox"""
        def task():
                # 1. Start the progress bar
                self.main_frame.progressbar.start()
                self.updateTextbox.update_textbox(">>> Running Ansible Ping...")

                # 2. Define the command
                # Uses your auto-generated inventory file
                cmd = ["ansible", "all", "-m", "ping", "-i", "./myansible/setupSSH/docker-inventory.ini"]

                try:
                # 3. Execute the command
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        
                        # 4. Show the result in the textbox
                        if result.stdout:
                                self.updateTextbox.update_textbox(result.stdout)
                        if result.stderr:
                                self.updateTextbox.update_textbox(f"Errors:\n{result.stderr}")
                        
                except Exception as e:
                        self.updateTextbox.update_textbox(f"Execution Error: {str(e)}")
                finally:
                        # 5. Stop the progress bar
                        self.main_frame.progressbar.stop()

        # Run in a thread so your GUI doesn't freeze
        threading.Thread(target=task, daemon=True).start()

    def run_playbook(self):
        # 1. Get the list of selected playbooks
        run_playbook_list = self.main_frame.inventory_tab.selected_playbook()
                
        if not run_playbook_list:
            self.updateTextbox.update_textbox("[System] No tasks selected to run.")
            return
        
        def task_thread():
            self.main_frame.progressbar.start()
        
        # Use a dictionary to map the ID (index 2) to the file path
            playbook_map = {
                "1": "./myansible/setupSSH/playbooks/update.yml",
                "2": "./myansible/setupSSH/playbooks/install_tools.yml",
                "3": "./myansible/setupSSH/playbooks/setup_nginx.yml"
            }
            for row in run_playbook_list:
                item_id = str(row[2]) # Convert index 2 to string for mapping
                
                if item_id in playbook_map:
                        playbook_path = playbook_map[item_id]
                        self.updateTextbox.update_textbox(f"\n>>> Starting Playbook: {playbook_path}")
                        cmd = [
                                "ansible-playbook", 
                                "-i", "./myansible/setupSSH/docker-inventory.ini", 
                                playbook_path, 
                                "--become"
                        ]
                        try:
                                process = subprocess.Popen(
                                        cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        text=True,
                                        bufsize=1,
                                        universal_newlines=True
                                )
                                # Read output line by line as it happens
                                for line in process.stdout:
                                # Use .after to ensure GUI updates safely from a thread
                                        self.master.after(0, lambda l=line: self.updateTextbox.update_textbox(l.strip()))
                        
                                process.wait() # Wait happens AFTER the loop finishes reading
                                self.updateTextbox.update_textbox(f">>> Finished Task {item_id}")
                        except Exception as e:
                                self.updateTextbox.update_textbox(f"[Error] Execution failed: {str(e)}")
        
                self.main_frame.progressbar.stop()
                self.updateTextbox.update_textbox("\n[System] All selected playbooks finished.")
        # Start the background thread
        threading.Thread(target=task_thread, daemon=True).start()