import customtkinter as ctk
from CTkTable import *

class DockerStatusCheckTab( ) :
    def __init__( self, docker_tab ) :
        self.ts_tab = docker_tab.add( 'Status' )
        self.setup_ui( )

    def setup_ui( self ) :
        self.info_label = ctk.CTkLabel(
            self.ts_tab,
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
            self.ts_tab,
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
            self.ts_tab,
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
        self.left_frame.grid_rowconfigure( 2, weight = 0 )
        self.left_frame.grid_rowconfigure( 3, weight = 0 )
        self.left_frame.grid_rowconfigure( 4, weight = 0 )
        self.left_frame.grid_rowconfigure( 5, weight = 0 )
        self.left_frame.grid_rowconfigure( 6, weight = 0 )
        self.left_frame.grid_rowconfigure( 7, weight = 0 )

        self.check_label = ctk.CTkLabel(
            self.left_frame,
            text = "What you want to check? ^_^''",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                overstrike=False
            )
        )
        self.check_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 20, 20 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )

### Check Box
        self.check_connection = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker Connection",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
                size=15,
            )
        )
        self.check_connection.grid(
            row = 1,
            column = 0,
            sticky = 'w' ,
            pady = ( 20, 20 ),
            padx = ( 40, 0 ),
        )

        self.docker_cli_version = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker CLI Version",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
                size=15,
            )
        )
        self.docker_cli_version.grid(
            row = 1,
            column = 1,
            sticky = 'w' ,
            pady = ( 20, 20 ),
            padx = ( 15, 0 ),
        )

        self.docker_server_version = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker Server Version",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
                size=15,
            )
        )

        # self.docker_server_version.grid(
        #     row = 1,
        #     column = 1,
        #     sticky = 'w' ,
        #     pady = ( 20, 20 ),
        #     padx = ( 10, 20 ),
        # )

        self.docker_context = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker context",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )

        # self.docker_context.grid(
        #     row = 2,
        #     column = 0,
        #     sticky = 'w' ,
        #     pady = ( 20, 20 ),
        #     padx = ( 40, 0 ),
        # )

        self.docker_info = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker Info",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )
        # self.docker_info.grid(
        #     row = 2,
        #     column = 1,
        #     sticky = 'w' ,
        #     pady = ( 20, 20 ),
        #     padx = ( 10, 0 ),
        # )

        self.docker_networks = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Docker Networks",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )

        self.docker_networks.grid(
            row = 2,
            column = 0,
            sticky = 'w' ,
            pady = ( 20, 20 ),
            padx = ( 40, 0 ),
        )

        self.running_containers = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Running Containers",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )
        self.running_containers.grid(
            row = 2,
            column = 1,
            sticky = 'w' ,
            pady = ( 20, 20 ),
            padx = ( 15, 0 ),
        )

        self.container_inspect = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Container Inspect",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )
        self.container_inspect.grid(
            row = 3,
            column = 0,
            sticky = 'w',
            pady = ( 20, 20 ),
            padx = ( 40, 0 ),
        )


        self.container_inspect_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "input container id or name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.container_inspect_entry.grid(
            row = 3,
            column = 1,
            sticky = 'we' ,
            pady = ( 20, 20 ),
            padx = ( 10, 20 ),
        )

        # self.image_inspect = ctk.CTkCheckBox(
        #     self.left_frame ,
        #     text = "Image Inspect",
        #     onvalue = "on",
        #     offvalue = "off",
        #     font = ctk.CTkFont(
        #     size=15,
        #     )
        # )
        # self.image_inspect.grid(
        #     row = 5,
        #     column = 0,
        #     sticky = 'w' ,
        #     pady = ( 20, 20 ),
        #     padx = ( 40, 0 ),
        # )

        # self.image_inspect_entry = ctk.CTkEntry(
        #     self.left_frame ,
        #     placeholder_text = "input image id or name",
        #     font = ctk.CTkFont(
        #         size=15,
        #     )
        # )

        # self.image_inspect_entry.grid(
        #     row = 5,
        #     column = 1,
        #     sticky = 'we' ,
        #     pady = ( 20, 20 ),
        #     padx = ( 10, 20 ),
        # )

        self.network_inspect = ctk.CTkCheckBox(
            self.left_frame ,
            text = "Network Inspect",
            onvalue = "on",
            offvalue = "off",
            font = ctk.CTkFont(
            size=15,
            )
        )
        self.network_inspect.grid(
            row = 4,
            column = 0,
            sticky = 'w' ,
            pady = ( 20, 20 ),
            padx = ( 40, 0 ),
        )

        self.network_inspect_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "input image id or name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.network_inspect_entry.grid(
            row = 4,
            column = 1,
            sticky = 'we' ,
            pady = ( 20, 20 ),
            padx = ( 10, 20 ),
        )

        self.check_it_out = ctk.CTkButton( 
            self.left_frame, 
            text="CHECK IT OUT",
            width = 200,
            height = 40,
            font = ctk.CTkFont( "Segoe Script", 18 ),
        )
        self.check_it_out.grid( 
            row = 5,
            column = 0,
            columnspan = 2,
            sticky = 'we' ,
            pady = ( 35 , 10 ),
            padx = ( 10, 10 ),
        )
        self.clear_btn = ctk.CTkButton( 
            self.left_frame, 
            text="@_@ CLEAR @_@",
            width = 200,
            height = 40,
            font = ctk.CTkFont( "Segoe Script", 18 ),
        )
        self.clear_btn.grid( 
            row = 6,
            column = 0,
            columnspan = 2,
            sticky = 'we' ,
            pady = ( 35 , 10 ),
            padx = ( 10, 10 ),
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
            [ "ID", "Names" ],
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
            padx= ( 50, 0 ),
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
            [ "Network ID", "Names" ],
            [ '41ecd807f659', 'docker_network_123' ],
            [ '22a4550ffe7a', 'bridge' ],
            [ '10f57fa303b9', 'host' ],
            [ 'c683be21172b', 'my_docker_network' ],
            [ '2b7ee5201314', 'nonw' ],
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
            padx= ( 50, 0 ),
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
