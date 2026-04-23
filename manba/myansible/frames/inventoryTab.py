import customtkinter as ctk
from CTkTable import *
import docker
import subprocess

class AnsibleInventoryTab :
    
    def __init__( self, ansible_tab ) :
        self.ansible_tab = ansible_tab.add( 'Operations' )
        self.client = docker.from_env( )


        self._setup_ui( )

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

    def _setup_ui( self ) :

        self.ansible_label = ctk.CTkLabel(
            self.ansible_tab,
            text = " Multi-Container Operation ",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                slant="italic",
                underline=True,
                overstrike=False
            )
        )

        self.ansible_label.pack(
            pady = 5 ,
            padx = 5 ,
        )

        self.left_frame = ctk.CTkFrame(
            self.ansible_tab,
            corner_radius = 10,
            
        )
        self.left_frame.pack(
            side = 'left',
            fill = 'both',
            expand = True,
            padx = ( 20, 20 ),
            pady = ( 20, 20 ),
        )

        self.right_frame = ctk.CTkFrame(
            self.ansible_tab,
            corner_radius = 10,
            
        )
        self.right_frame.pack(
            side = 'right',
            fill = 'both',
            expand = True,
            padx = ( 0, 20 ),
            pady = ( 20, 20 ),
        )


##### Left Frame
        self.left_frame.grid_columnconfigure( 0, weight = 1 )
        self.left_frame.grid_columnconfigure( 1, weight = 1 )
        self.left_frame.grid_rowconfigure( 0, weight = 0 )
        self.left_frame.grid_rowconfigure( 1, weight = 0 )


        self.inventory_label = ctk.CTkLabel(
            self.left_frame,
            text = "Select containers",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.inventory_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 10, 5 ),
            padx = ( 20, 20 ),
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
                                        "stoped" if container["status"].lower() == "exited" else container["status"] ,
                ]

        self.container_info_table = CTkTable( 
                master = self.left_frame,
                values = self.container_list,
                width = 50,
                command = self.on_table_click

            )

        self.container_info_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 20, 20 ),
            pady = ( 20, 15 ),
            sticky = "nsew"            
        )

        self.create_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Try Ping",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.create_btn.grid( 
            row = 2,
            column = 0,
            columnspan = 2,
            sticky = 'ne' ,
            pady = ( 10 , 10 ),
            padx = ( 0, 20 ),
        )


##### Right Frame
        self.select_app_label = ctk.CTkLabel(
            self.right_frame,
            text = "Select Action",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.select_app_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 20, 10 ),
            padx = ( 60, 10 ),
            sticky = 'ew',
        )

        # For demo Only
        test_list = [
            [ 'Select', "Action", "Priority"],
            [ '▢', 'System Update', "1" ],
            [ '▢', 'Install vim', "2"],
            [ '▢', 'Install ip-utils', "3" ],
            [ '▢', 'Install xxx', "4" ],
            [ '▢', 'Install xxx', "5" ],
            [ '▢', 'Install xxx', "6" ],
            [ '▢', 'Install xxx', "7" ],
            [ '▢', 'Install xxx', "8" ],
            [ '▢', 'Install xxx', "9" ],
            [ '', '', "" ],
            [ '', '', "" ],
            [ '', '', "" ],
            [ '', '', "" ],
            [ '', '', "" ],
            [ '', '', "" ],
        ]

        self.show_table = CTkTable( 
                master = self.right_frame,
                # header_color = '',
                values = test_list,
                width = 100
            )
        self.show_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 70, 0 ),
            pady = ( 0, 50 ),
            sticky = "ew"
        )

        self.run_btn = ctk.CTkButton( 
            self.right_frame, 
            text="RUN",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.run_btn.grid(
            row = 2,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 0 , 30 ),
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
    
    def selected_container( self ) :
        select_list = list()
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            for column_idx, column in enumerate( row ) :
                if column == '🗹' :
                    select_list.append( self.container_list[row_idx] )
        return select_list
    
    def refrest_container_list( self ) :
        self.container_list.clear()
        container_headers =  [ "Select", "Name", "Status" ]
        self.container_list.append( container_headers )
        all_container_info = self.show_all_containers( )
        if all_container_info :
            for container in all_container_info :
                self.container_list.append( [ "▢", 
                                            container['name'], 
                                            "stoped" if container["status"].lower() == "exited" else container["status"],
                                            ] )

        self.container_info_table.update_values( self.container_list )