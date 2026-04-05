import customtkinter as ctk

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
                """Welcome to Docker Management Tool!\nInfo remark"""
        )        

    def on_tab_changed( self ) :

        self.current_tab_name = self.docker_tab.get()

        self.remark.delete("0.0", "end")

        if self.current_tab_name == "Info" :
            self.remark.insert( 
                "0.0",
                "Welcome to Docker Management Tool!\nInfo remark"
        )
        elif self.current_tab_name == "Image" :
            self.remark.insert( 
                "0.0",
                "Welcome to Docker Management Tool!\nImage remark"
        )
        elif self.current_tab_name == "Container" :
            self.remark.insert( 
                "0.0",
                """Welcome to Docker Management Tool!\nContainer remark"""
        )
        elif self.current_tab_name == "Network" :
            self.remark.insert( 
                "0.0",
                """Welcome to Docker Management Tool!\nNetwork remark"""
        )
        elif self.current_tab_name == "Trobleshoot" :
            self.remark.insert( 
                "0.0",
                """Welcome to Docker Management Tool!\nTrobleshoot remark"""
        )

