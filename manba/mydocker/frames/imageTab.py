import customtkinter as ctk
from CTkTable import *
import webbrowser

class DockerImageTab :
    def __init__( self, docker_tab ) :
        self.image_tab = docker_tab.add( 'Image' )
        self._setup_ui( )

    def _setup_ui( self ) :

        self.image_label = ctk.CTkLabel(
            self.image_tab,
            text = "Docker Image Management",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                slant="italic",
                underline=True,
                overstrike=False
            )
        )

        self.image_label.pack(
            pady = 5 ,
            padx = 5 ,
        )

        self.left_frame = ctk.CTkFrame(
            self.image_tab,
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
            self.image_tab,
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
        self.left_frame.grid_rowconfigure( 0, weight = 1 )
        self.left_frame.grid_rowconfigure( 1, weight = 1 )
        self.left_frame.grid_rowconfigure( 2, weight = 1 )
        self.left_frame.grid_rowconfigure( 3, weight = 1 )
        self.left_frame.grid_rowconfigure( 4, weight = 1 )
        self.left_frame.grid_rowconfigure( 5, weight = 1 )

        self.image_label = ctk.CTkLabel(
            self.left_frame,
            text = "To Create Docker Container",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.image_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 20, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )

### Create Docker Container
        self.image_name_label = ctk.CTkLabel(
            self.left_frame,
            text = "Image name: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.image_name_label.grid(
            row = 1,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.image_name_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "image name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.image_name_entry.grid(
            row = 1,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )
#
        self.image_version_label = ctk.CTkLabel(
            self.left_frame,
            text = "Image version: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.image_version_label.grid(
            row = 2,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.image_version_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "latest by default ",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.image_version_entry.grid(
            row = 2,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        self.image_command_label = ctk.CTkLabel(
            self.left_frame,
            text = "Full command:",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.image_command_label.grid(
            row = 3,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 0 ),
            padx = ( 40, 0 ),
        )

        self.image_command_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "docker pull image...",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.image_command_entry.grid(
            row = 3,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 0 ),
            padx = ( 0, 20 ),
        )

        # self.image_removal_label = ctk.CTkLabel(
        #     self.left_frame,
        #     text = "Remove Image:",
        #     font = ctk.CTkFont(
        #         family="Arial",
        #         size=16,
        #         weight="bold",
        #         overstrike=False
        #     )
        # )

        # self.image_removal_label.grid(
        #     row =4,
        #     column = 0,
        #     sticky = 'w' ,
        #     pady = ( 25 , 0 ),
        #     padx = ( 40, 0 ),
        # )

        # self.image_removal_entry = ctk.CTkEntry(
        #     self.left_frame ,
        #     placeholder_text = "remove by name or id",
        #     font = ctk.CTkFont(
        #         size=15,
        #     )
        # )

        # self.image_removal_entry.grid(
        #     row = 4,
        #     column = 1,
        #     sticky = 'we' ,
        #     pady = ( 25 , 0 ),
        #     padx = ( 0, 20 ),
        # )

        self.docker_hub_label = ctk.CTkLabel(
            self.left_frame,
            text = "Go to Docker Hub:",
            font = ctk.CTkFont(
                family="Arial",
                size = 16,
                weight="bold",
                overstrike=False
            )
        )
        self.docker_hub_label.grid(
            row =4,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 20 ),
            padx = ( 40, 0 ),
        )

        self.docker_hub_btn = ctk.CTkButton(
            self.left_frame,
            text = "DockerHub",
            command = self.open_docker_hub,
        )

        self.image_removal_label = ctk.CTkLabel(
            self.left_frame,
            text = "Remove Docker Image:",
            font = ctk.CTkFont(
                family="Arial",
                size = 16,
                weight="bold",
                overstrike=False
            )
        )

        self.docker_hub_btn.grid(
            row = 4,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 20 ),
            padx = ( 0, 20 ),
        )

        self.docker_hub_label.grid(
            row =4,
            column = 0,
            sticky = 'w' ,
            pady = ( 25 , 20 ),
            padx = ( 40, 0 ),
        )

        self.docker_hub_btn = ctk.CTkButton(
            self.left_frame,
            text = "DockerHub",
            command = self.open_docker_hub,
        )

        self.docker_hub_btn.grid(
            row = 4,
            column = 1,
            sticky = 'we' ,
            pady = ( 25 , 20 ),
            padx = ( 0, 20 ),
        )
        self.image_execute = ctk.CTkButton( 
            self.left_frame, 
            text="PULL",
            width = 250,
            height = 50,
            font = ctk.CTkFont( "Segoe Script", 20 ),
        )
        self.image_execute.grid( 
            row = 5,
            column = 0,
            columnspan = 2,
            sticky = 'we' ,
            pady = ( 10 , 20 ),
            padx = ( 10, 10 ),
        )

##### Right Frame
        self.show_image_label = ctk.CTkLabel(
            self.right_frame,
            text = "Docker image information",
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
            pady = ( 20, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )

        # For demo Only
        test_image_list = [
            [ 'Select',"ID", "Names" ,"Tag"],
            [ '▢','2b7c51034242', 'hello', 'latest' ],
            [ '▢','2b7c51034242', 'ubuntu', 'latest' ],
            [ '▢','2b7c51034242', 'nginx', 'alpine' ],
            [ '▢','2b7c51034242', 'nginx', 'latest' ],
            [ '▢','2b7c51034242', 'hello-world', 'latest' ],
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
            padx= ( 40, 0 ),
            pady = ( 10, 0 ),
            sticky = "nsew"            
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


### Command
    def open_docker_hub( self ) :
        webbrowser.open_new( 'https://hub.docker.com' )