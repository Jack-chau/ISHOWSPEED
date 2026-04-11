import customtkinter as ctk
from CTkTable import *
import webbrowser

class DockerNetworkTab :
    def __init__( self, docker_tab ) :
        self.network_tab = docker_tab.add( 'Network' )
        self._setup_ui( )

    def _setup_ui( self ) :

        self.network_label = ctk.CTkLabel(
            self.network_tab,
            text = "Docker network Management",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                slant="italic",
                underline=True,
                overstrike=False
            )
        )

        self.network_label.pack(
            pady = 5,
            padx = 5,
        )

        self.left_frame = ctk.CTkFrame(
            self.network_tab,
            width = 700,
            height = 100,
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
            self.network_tab,
            width = 300,
            height = 100,
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
        self.left_frame.grid_columnconfigure( 1, weight = 0 )
        self.left_frame.grid_rowconfigure( 0, weight = 0 )
        self.left_frame.grid_rowconfigure( 1, weight = 0 )
        self.left_frame.grid_rowconfigure( 2, weight = 0 )
        self.left_frame.grid_rowconfigure( 3, weight = 0 )
        self.left_frame.grid_rowconfigure( 4, weight = 0 )
        self.left_frame.grid_rowconfigure( 5, weight = 0 )
        self.left_frame.grid_rowconfigure( 6, weight = 0 )
        self.left_frame.grid_rowconfigure( 7, weight = 0 )
        self.left_frame.grid_rowconfigure( 8, weight = 0 )
        self.left_frame.grid_rowconfigure( 9, weight = 0 )
        self.left_frame.grid_rowconfigure( 10, weight = 0 )
        self.left_frame.grid_rowconfigure( 11, weight = 0 )
        
        self.create_delete_label = ctk.CTkLabel(
            self.left_frame,
            text = "Create or Delete Docker Network",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.create_delete_label.grid(
            row =0,
            column = 0,
            columnspan = 2,
            sticky = 'ew' ,
            pady = ( 25 , 0 ),
            padx = ( 10, 10 ),
        )

# Create Docker Network
        self.create_network_label = ctk.CTkLabel(
            self.left_frame,
            text = "Create docker network:",
            font = ctk.CTkFont(
                family="Arial",
                size = 16,
                weight="bold",
                overstrike=False
            )
        )
        self.create_network_label.grid(
            row =1,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.create_network_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "New network name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.create_network_entry.grid(
            row = 1,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.subnet_label = ctk.CTkLabel(
            self.left_frame,
            text = "Subnet:",
            font = ctk.CTkFont(
                family="Arial",
                size = 16,
                weight="bold",
                overstrike=False
            )
        )
        self.subnet_label.grid(
            row = 2,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.subnet_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "172.18.0.0/16",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.subnet_entry.grid(
            row = 2,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.gateway_label = ctk.CTkLabel(
            self.left_frame,
            text = "Gateway:",
            font = ctk.CTkFont(
                family="Arial",
                size = 16,
                weight="bold",
                overstrike=False
            )
        )
        self.gateway_label.grid(
            row =3,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.gateway_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "172.18.0.1",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.gateway_entry.grid(
            row = 3,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        # self.create_network_execute = ctk.CTkButton( 
        #     self.left_frame, 
        #     text="Execute",
        #     width = 140,
        #     height = 40,
        #     font = ctk.CTkFont( "Segoe Script", 15 ),
        # )
        # self.create_network_execute.grid( 
        #     row = 4,
        #     column = 0,
        #     columnspan = 2,
        #     sticky = 'e' ,
        #     pady = ( 10 , 0 ),
        #     padx = ( 10, 20 ),
        # )

# Delect Docker Network
        # self.network_delete = ctk.CTkLabel(
        #     self.left_frame,
        #     text = "Delete Docker Network",
        #     font = ctk.CTkFont(
        #         family="Courier New",
        #         size=18,
        #         weight="bold",
        #         overstrike=False
        #     )
        # )
        # self.network_delete.grid(
        #     row =5,
        #     column = 0,
        #     columnspan = 2,
        #     sticky = 'ew' ,
        #     pady = ( 25 , 0 ),
        #     padx = ( 10, 10 ),
        # )

        # self.delete_label = ctk.CTkLabel(
        #     self.left_frame,
        #     text = "Delete network:",
        #     font = ctk.CTkFont(
        #         family="Arial",
        #         size = 16,
        #         weight="bold",
        #         overstrike=False
        #     )
        # )
        # self.delete_label.grid(
        #     row =4,
        #     column = 0,
        #     sticky = 'w' ,
        #     pady = ( 25 , 0 ),
        #     padx = ( 40, 0 ),
        # )

        # self.delete_entry = ctk.CTkEntry(
        #     self.left_frame ,
        #     placeholder_text = "network idx",
        #     font = ctk.CTkFont(
        #         size=15,
        #     )
        # )

        # self.delete_entry.grid(
        #     row = 4,
        #     column = 1,
        #     sticky = 'we' ,
        #     pady = ( 25 , 0 ),
        #     padx = ( 0, 20 ),
        # )

        self.create_network_execute = ctk.CTkButton( 
            self.left_frame, 
            text="Create",
            width = 140,
            height = 40,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.create_network_execute.grid( 
            row = 4,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 10 , 0 ),
            padx = ( 10, 20 ),
        )

### Assign Static IP
        self.staticIP_label = ctk.CTkLabel(
            self.left_frame,
            text = "Assign Static IP to Container",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.staticIP_label.grid(
            column = 0,
            row = 6,
            columnspan = 2,
            pady = ( 20, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )
        self.assign_container_label = ctk.CTkLabel(
            self.left_frame,
            text = "Container Name: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.assign_container_label.grid(
            row = 7,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.assign_container_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "container idx",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.assign_container_entry.grid(
            row = 7,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.network_name_label = ctk.CTkLabel(
            self.left_frame,
            text = "Network: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.network_name_label.grid(
            row = 8,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.network_name_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "my_docker_network",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.network_name_entry.grid(
            row = 8,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.static_ip_label = ctk.CTkLabel(
            self.left_frame,
            text = "Static IP:",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.static_ip_label.grid(
            row = 9,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.static_ip_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "172.18.0.xxx",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.static_ip_entry.grid(
            row = 9,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.staticIp_execute = ctk.CTkButton( 
            self.left_frame, 
            text="Execute",
            width = 140,
            height = 40,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.staticIp_execute.grid( 
            row = 10,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 20 , 0 ),
            padx = ( 10, 20 ),
        )

##### Right Frame
        self.id_label = ctk.CTkLabel(
            self.right_frame,
            text = "Container ID",
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

        # For demo Only
        test_id_list = [
            [  "ID", "Names" ],
            [ '2b7c51034242', 'nginx02' ],
            [ '2b7c51034242', 'nginx01' ],
            [ '2b7c51034242', 'my_web_server' ],
            [ '2b7c51034242', 'ubuntu02' ],
            [ '2b7c51034242', 'ubuntu01' ],
        ]

        self.check_id_table = CTkTable( 
                master = self.right_frame,
                values = test_id_list,
                width = 80
            )
        self.check_id_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 20, 0 ),
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
            row = 2,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 10 ),
        )


        self.network_label = ctk.CTkLabel(
            self.right_frame,
            text = "Docker Network",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.network_label.grid(
            row = 3,
            column = 0,
            columnspan = 2,
            pady = ( 30, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )
        
        test_network_list = [
            [ 'Select',"Network ID", "Names" ],
            [ '▢','41ecd807f659', 'docker_network_123' ],
            [ '▢','22a4550ffe7a', 'bridge' ],
            [ '▢','10f57fa303b9', 'host' ],
            [ '▢','c683be21172b', 'my_docker_network' ],
            [ '▢','2b7ee5201314', 'nonw' ],
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
            padx= ( 20, 0 ),
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
