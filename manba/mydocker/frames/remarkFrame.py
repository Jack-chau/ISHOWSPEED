import customtkinter as ctk
import textwrap


# Remark content
_info_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Info Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • Quick Container Management\n
            • Image Version Preview\n
            • Docker Network Setting\n
            Ready to manage your Docker!
    """)

_image_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Image Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • Pull official image\n
            • Defalt latest verion \n
            • Pull image by command\n
            Ready to manage your Docker!
    """)

_container_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Container Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • Create Container\n
            • Start Container\n
            • Stop Container\n
            • Remove Container\n
            Ready to manage your Docker!
    """)

_networke_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Image Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • Create Docker Network\n
            • Assign Network to Container\n
            • Setup Static IP\n
            • DHCP by Default\n
            Ready to manage your Docker!
    """)
_trobleshooting_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Image Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • View Docker Static\n
            • Inspect Container\n
            • Inspect Docker Network\n
            Ready to manage your Docker!
    """)

class RemarkManager :
    def __init__( self, docker_tab, remark_frame ) :
        self.remark_frame = remark_frame
        self.docker_tab = docker_tab
        self.docker_tab.configure( command = self.on_tab_changed )
        self.setup_ui( )



    def setup_ui( self ) :
# Create remark frame
        self.remark_iner_frame = ctk.CTkFrame( 
            self.remark_frame,
            width = 400,
            # border_width = 2,
        )

        self.remark_iner_frame.grid( 
            row = 0, 
            column = 7,
            columnspan = 2,
            rowspan = 2,
            sticky = 'nsew',
        )

# Remark
        self.remark_tab = ctk.CTkTabview(
            self.remark_iner_frame,
            width = 400,
            height = 500,
        )
        self.remark_tab.pack(
            fill = 'both' ,
            expand = True,
            side = 'top',
            padx = ( 0, 0 ),
            pady = ( 0, 0 )
        )

        self.remark_tab.add( 'Remarks' )
        
        self.remark_scroll_frame = ctk.CTkScrollableFrame(
            self.remark_tab.tab( 'Remarks' ),
            height = 750,
            width = 380,
        )
        self.remark_scroll_frame.grid(
            row = 0,
            column = 0,
            columnspan = 4,
            rowspan = 2,
            padx= ( 10, 0 ),
            pady = ( 10, 0 ),
            sticky = "nsew" 
        )

        self.remark_label = ctk.CTkLabel(
            self.remark_scroll_frame,
            text = "Docker Management: ",
            font = ( "Comic Sans MS", 30 ),
        )
        self.remark_label.grid(
            row = 0, 
            column = 0, 
            columnspan = 4,
            padx = ( 10, 0 ), 
            pady = ( 20, 0 ), 
            sticky = "nsew",
        )

        self.remark = ctk.CTkTextbox(
            self.remark_scroll_frame, 
            font = ( "Comic Sans MS", 25 ),
            width = 400,
            height = 700,
            fg_color = ["#C0C8CE", "#2B2D2F"],
        )
        self.remark.grid(
            row = 2,
            rowspan = 2,
            column = 0, 
            columnspan = 4,
            padx = ( 10, 0 ), 
            pady = ( 20, 0 ), 
            sticky = "nsew",
        )

        self.remark.insert( 
                "0.0",
                _info_content
        )        

    def on_tab_changed( self ) :

        self.current_tab_name = self.docker_tab.get()

        self.remark.delete("0.0", "end")

        if self.current_tab_name == "Info" :
            self.remark.insert( 
                "0.0",
                _info_content
        )

        elif self.current_tab_name == "Image" :
            self.remark.insert( 
                "0.0",
                _image_content
        )
        elif self.current_tab_name == "Container" :
            self.remark.insert( 
                "0.0",
                _container_content
        )
        elif self.current_tab_name == "Network" :
            self.remark.insert( 
                "0.0",
                _networke_content
        )
        elif self.current_tab_name == "Trobleshoot" :
            self.remark.insert( 
                "0.0",
                _trobleshooting_content
        )

