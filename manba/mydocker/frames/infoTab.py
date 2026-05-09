import customtkinter as ctk
from CTkTable import *
from CTkMessagebox import CTkMessagebox
import docker
import subprocess

class DockerInfoTab( ) :
    def __init__( self, docker_tab ) :
        self.info_tab = docker_tab.add( 'Info' )
        self.client = docker.from_env( )

        self.setup_ui( )

    def show_all_containers( self ) :
        all_containers = self.client.containers.list( all = all )
        all_containers_list = list( )
        for container in all_containers :
            all_containers_list.append(
                {
                    'name' : container.name,
                    'status' : container.status,
                }
            )
        if len( all_containers_list ) > 0 :
            return ( all_containers_list )


    def setup_ui( self ) :
        self.info_label = ctk.CTkLabel(
            self.info_tab,
            text = "Hello! Welcome to check docker information!",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                slant="italic",
                underline=True,
                overstrike=False
            )
        )
    
        self.info_label.pack(
            pady = 5 ,
            padx = 5 ,
        )

        self.left_frame = ctk.CTkFrame(
            self.info_tab,
            corner_radius = 10,
            
        )
        self.left_frame.pack(
            side = 'left',
            fill = 'both',
            expand = True,
            padx = ( 20, 0 ),
            pady = ( 20, 20 ),
        )

        self.right_frame = ctk.CTkFrame(
            self.info_tab,
            corner_radius = 10,
            
        )
        self.right_frame.pack(
            side = 'right',
            fill = 'both',
            expand = True,
            padx = ( 20, 20 ),
            pady = ( 20, 20 ),
        )

##### Left Frame
        self.left_frame.grid_columnconfigure( 0, weight = 1 )
        self.left_frame.grid_columnconfigure( 1, weight = 1 )
        self.left_frame.grid_rowconfigure( 0, weight = 0 )
        self.left_frame.grid_rowconfigure( 1, weight = 0 )

        self.id_label = ctk.CTkLabel(
            self.left_frame,
            text = "Running Container",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                overstrike=False
            )
        )
        self.id_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 20, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )

#  Container Management Table
        self.container_list = list( )
        container_headers = [ 'Select', 'Name', 'Status' ]

        self.container_list.append( container_headers )

        # Extract data to a 2D array
        all_containers_info = self.show_all_containers( )
        for i in range( 13 ) :
            self.container_list.append( [] )
        if all_containers_info : 
            for i, container in enumerate( all_containers_info, 1 ) :
                self.container_list[ i ] = [
                                        "▢", 
                                        container['name'], 
                                        "stopped" if container["status"].lower() == "exited" else container["status"] ,
                ]

        self.container_info_table = CTkTable( 
                master = self.left_frame,
                values = self.container_list,
                width = 80,
                command = self.on_table_click

            )

        self.container_info_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 20, 20 ),
            pady = ( 10, 0 ),
            sticky = "nsew"            
        )

# Run Container
        self.run_container_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Run",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.run_container
        )
        self.run_container_btn.grid( 
            row = 3,
            column = 0,
            columnspan = 2,
            sticky = 'w' ,
            pady = ( 35 , 0 ),
            padx = ( 30, 10 ),
        )

# Stop Container
        self.stop_container_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Stop",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.stop_container
        )
        self.stop_container_btn.grid( 
            row = 3,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 0, 20 ),
        )
# Remove 
        self.remove_container_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Remove",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.remove_container
        )
        self.remove_container_btn.grid( 
            row = 4,
            column = 0,
            columnspan = 2,
            sticky = 'w' ,
            pady = ( 35 , 0 ),
            padx = ( 30, 10 ),
        )
        
# Refrash Table
        self.refrash_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Refresh",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.refrest_container_list
        )
        self.refrash_btn.grid( 
            row = 4,
            column = 1,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 0, 20 ),
        )

##### Right Frame
        self.show_image_label = ctk.CTkLabel(
            self.right_frame,
            text = "Docker Image",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.show_image_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 20, 10 ),
            padx = ( 60, 10 ),
            sticky = 'ew',
        )

        # For demo Only
        test_image_list = [
            [ 'Select', "Names" ,"Tag"],
            [ '▢', 'hello', 'latest' ],
            [ '▢', 'ubuntu', '23.5.3' ],
            [ '▢', 'nginx', 'alpine' ],
            [ '▢', 'nginx', '2.3.1' ],
            [ '▢', 'hello-world', 'latest' ],
        ]

        self.show_image_table = CTkTable( 
                master = self.right_frame,
                # header_color = '',
                values = test_image_list,
                width = 100
            )
        self.show_image_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 70, 0 ),
            pady = ( 0, 50 ),
            sticky = "ew"            
        )

        self.network_label = ctk.CTkLabel(
            self.right_frame,
            text = "Docker Network",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )

        self.network_label.grid(
            row = 3,
            column = 0,
            columnspan = 2,
            padx = ( 60, 10 ),
            pady = ( 30, 0 ),
            sticky = 'ew',
        )
        
        test_network_list = [
            [ 'Select', "Names" ],
            [ '▢', 'network_123' ],
            [ '▢', 'bridge' ],
            [ '▢', 'host' ],
            [ '▢', 'my_network' ],
            [ '▢', 'none' ],
        ]

        self.test_network_list = CTkTable( 
                master = self.right_frame,
                values = test_network_list,
                width = 130
            )
        self.test_network_list.grid(
            row = 4,
            column = 0,
            columnspan = 2,
            padx= ( 70, 0 ),
            pady = ( 10, 0 ),
            sticky = "ew"            
        )

        self.refrash_btn = ctk.CTkButton( 
            self.right_frame, 
            text="Refresh",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.refrash_btn.grid( 
            row = 5,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 0 ),
        )

    def on_table_click( self, cell ) :
        row, column = cell["row"] , cell["column"]
        if row > 0 and column == 0:
            if self.container_list[row][0] == '▢' :
                self.container_list[row][0] = '🗹'
            else :
                self.container_list[row][0] = '▢'
            self.container_info_table.update_values( self.container_list )
        else :
            pass
    
    def selected_container( self ) :
        select_list = list()
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            for column_idx, column in enumerate( row ) :
                if column == '🗹' :
                    select_list.append( self.container_list[row_idx] )
        return select_list
    
    def run_container( self ) :
        run_name_list = list()
        err_list = list()
        result = ''
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            if len(row) > 1 and row[0] == '🗹' and row[2] != "running" :
                run_name_list.append( row[1] )
                action_name = row[1]
                print( f"Executing task: {action_name}" )


                    
        try:
            for i in err_list :
                result += f"The Container {i} is already running!!!\n"

            for i in run_name_list :
                    run_cont = subprocess.run( 
                        [ 'docker', 'start', str( i ) ],
                        capture_output = True,
                        text = True,
                    )
                    result += f"The Container {i} is runing!!!\n"
        except Exception as e :
            return( e )
        self.refrest_container_list()
        return result


    def stop_container( self ) :
        # self.refrest_container_list()
        stop_name_list = list()
        err_list = list()
        result = ''
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            if len(row) > 1 and row[0] == '🗹' and row[2] == "running" :
                stop_name_list.append( row[1] )
                    
        try:
            for i in err_list :
                result += f"The Container {i} is not running!!!\n"

            for i in stop_name_list :
                    run_cont = subprocess.run( 
                        [ 'docker', 'stop', str( i ) ],
                        capture_output = True,
                        text = True,
                    )
                    result += f"The Container {i} is stoped!!!\n"
        except Exception as e :
            return( e )
        self.refrest_container_list()
        return result
        
    def remove_container( self ) :
        # self.refrest_container_list()
        running_list = list()
        stoped_list = list()
        result = ''
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            if len(row) > 1 and row[0] == '🗹' and row[2] == "running" :
                running_list.append( row[1] )
            elif row[0] == '🗹' and row[2] != "running" :
                stoped_list.append( row[1] )

        if not running_list and not stoped_list :
            CTkMessagebox(
                title = "No Selection",
                message = "Please select at least one container to remove!",
                icon = "info",
                option_1 = "OK"
            )
            return
                    
        try:
            for i in stoped_list :
                message = f"Are you sure you want to remove { i } container?\n\n"
                msg = CTkMessagebox(
                    title = "Confirm Removal",
                    message = message,
                    icon = "warning",
                    option_1 = "Yes",
                    option_2 = "No"
                )
                if msg.get() == 'Yes' :
                    run_cont = subprocess.run( 
                            [ 'docker', 'rm', str( i ) ],
                            capture_output = True,
                            text = True,
                        )
                    result += f"The Container {i} is removed!!!\n"
                    self.refrest_container_list( )
                    CTkMessagebox(
                        title = "Success",
                        message = result,
                        icon = "check",
                        option_1 = "OK"
                    )
                else :
                    pass
            

            for i in running_list :
                message = f"Are you sure you want to remove { i } container?\n\n"
                msg = CTkMessagebox(
                    title = "Confirm Removal",
                    message = message,
                    icon = "warning",
                    option_1 = "Yes",
                    option_2 = "No"
                )
                if msg.get() == 'Yes' :
                    run_cont = subprocess.run( 
                        [ 'docker', 'stop', str( i ) ],
                        capture_output = True,
                        text = True,
                    )
                    run_cont = subprocess.run( 
                        [ 'docker', 'rm', str( i ) ],
                        capture_output = True,
                        text = True,
                    )
                    self.refrest_container_list( )
                    result += f"The Container {i} is removed!!!\n"
                    CTkMessagebox(
                        title = "Success",
                        message = result,
                        icon = "check",
                        option_1 = "OK"
                    )
                else :
                    continue

        except Exception as e :
            CTkMessagebox(
                    title="Error",
                    message=f"Error removing containers: {str(e)}",
                    icon="cancel",
                    option_1="OK"
                )
            return str(e)
                
        self.refrest_container_list()
        return result

    def refrest_container_list( self ) :
        self.container_list.clear()
        container_headers =  [ "Select", "Name", "Status" ]
        self.container_list.append( container_headers )
        all_container_info = self.show_all_containers( )
        if all_container_info :
            for container in all_container_info :
                self.container_list.append( [ "▢", 
                                            container['name'], 
                                            "stopped" if container["status"].lower() == "exited" else container["status"],
                                            ] )

        self.container_info_table.update_values( self.container_list )