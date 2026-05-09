import customtkinter as ctk
from CTkTable import *
from CTkMessagebox import CTkMessagebox
import webbrowser
import docker
import subprocess

class DockerContainerTab :
    def __init__( self, docker_tab ) :
        self.container_tab = docker_tab.add( 'Container' )
        self.client = docker.from_env( )
        self._setup_ui( )
        self.refrest_container_list( )

    # Show all containers
    def show_all_containers( self ) :
        all_containers = self.client.containers.list( all = all )
        all_containers_list = list( )
        for container in all_containers :
            containers_inspect = container.attrs['NetworkSettings']['Networks']
            # init variables
            network_name = "none"
            network_driver = "none"
            ip_address = "none"
            ports_str = "none"

            # Get network information if exists
            if containers_inspect :
                network_info = dict( )
                # for key and values in containers_inspect.items( )
                for network_name, network_setting in containers_inspect.items( ) :
                    try:
                        network_inspect = self.client.networks.get( network_setting[ 'NetworkID' ] )
                        network_info[network_name] = {
                            'driver' : network_inspect.attrs['Driver'],
                            'network_id' : network_inspect.id,
                            'ip_address' : network_setting.get( 'IPAddress', 'none' ),
                            }

                    except Exception as e:
                        print(f"Error getting network info: {e}")
                        continue

                if network_info :
                    network_name = list( network_info.keys() )[0]
                    network_driver = network_info[ network_name ][ 'driver' ]
                    ip_address = network_info[ network_name ][ 'ip_address' ]
                
            ports_info = container.attrs.get('NetworkSettings',{}).get( 'Ports', {} )
            ports_str = ', '.join(ports_info.keys()) if ports_info else "none"


            all_containers_list.append(
                {
					'id' : container.short_id,
					'name' : container.name,
					'status' : container.status,
					'newtwork_name' : network_name,
					'network_type' : network_driver,
					'ip_addr' : ip_address,
					'ports' : ports_str,
				}
			)
        if len( all_containers_list ) > 0 :
            return( all_containers_list )


    def _setup_ui( self ) :
        self.container_label = ctk.CTkLabel(
            self.container_tab,
            text = "Docker Container Management",
            font = ctk.CTkFont(
                family="Courier New",
                size=16,
                weight="bold",
                slant="italic",
                underline=True,
                overstrike=False
            )
        )

        self.container_label.pack(
            pady = 5 ,
            padx = 5 ,
        )

        self.left_frame = ctk.CTkFrame(
            self.container_tab,
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
            self.container_tab,
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
        self.left_frame.grid_rowconfigure( 6, weight = 1 )
        self.left_frame.grid_rowconfigure( 7, weight = 1 )
        self.left_frame.grid_rowconfigure( 8, weight = 1 )
        self.left_frame.grid_rowconfigure( 9, weight = 1 )

        self.container_label = ctk.CTkLabel(
            self.left_frame,
            text = "Create Container",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.container_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 10, 0 ),
            padx = ( 10, 10 ),
            sticky = 'ew',
        )

### Create Docker Container
# container_name
        self.name_label = ctk.CTkLabel(
            self.left_frame,
            text = "Container Name: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.name_label.grid(
            column = 0,
            row = 1,
            sticky = 'w' ,
            pady = ( 5 , 0 ),
            padx = ( 40, 0 ),
        )

        self.name_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "Container Name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.name_entry.grid(
            row = 1,
            column = 1,
            sticky = 'we' ,
            pady = ( 5 , 0 ),
            padx = ( 0, 20 ),
        )
# Container Image
        self.image_label = ctk.CTkLabel(
            self.left_frame,
            text = "Image: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.image_label.grid(
            column = 0,
            row = 2,
            sticky = 'w' ,
            pady = ( 5 , 0 ),
            padx = ( 40, 0 ),
        )

        self.image_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "Image:version",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.image_entry.grid(
            row = 2,
            column = 1,
            sticky = 'we' ,
            pady = ( 5 , 0 ),
            padx = ( 0, 20 ),
        )
# container network
        self.network_label = ctk.CTkLabel(
            self.left_frame,
            text = "Network Name: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.network_label.grid(
            column = 0,
            row = 3,
            sticky = 'w' ,
            pady = ( 5 , 0 ),
            padx = ( 40, 0 ),
        )

        self.network_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "Network Name",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.network_entry.grid(
            row = 3,
            column = 1,
            sticky = 'we' ,
            pady = ( 5 , 0 ),
            padx = ( 0, 20 ),
        )
# Containter Static Ip
        self.staticIP_label = ctk.CTkLabel(
            self.left_frame,
            text = "Static IP: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )

        self.staticIP_label.grid(
            column = 0,
            row = 4,
            sticky = 'w' ,
            pady = ( 5 , 0 ),
            padx = ( 40, 0 ),
        )

        self.staticIP_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "172.18.0.10",
            font = ctk.CTkFont(
                size=15,
            )
        )
        self.staticIP_entry.grid(
            row = 4,
            column = 1,
            sticky = 'we' ,
            pady = ( 5 , 0 ),
            padx = ( 0, 20 ),
        )

# container publish port
        self.pub_port_label = ctk.CTkLabel(
            self.left_frame,
            text = "Published Port: ",
            font = ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
                overstrike=False
            )
        )
        self.pub_port_label.grid(
            column = 0,
            row = 5,
            sticky = 'w' ,
            pady = ( 5 , 0 ),
            padx = ( 40, 0 ),
        )

        self.pub_port_entry = ctk.CTkEntry(
            self.left_frame ,
            placeholder_text = "hostport:container_port",
            font = ctk.CTkFont(
                size=15,
            )
        )

        self.pub_port_entry.grid(
            row = 5,
            column = 1,
            sticky = 'we' ,
            pady = ( 5 , 0 ),
            padx = ( 0, 20 ),
        )

        self.create_container_btn = ctk.CTkButton( 
            self.left_frame, 
            text="Create Container",
            width = 140,
            height = 40,
            font = ctk.CTkFont( "Segoe Script", 15 ),
        )
        self.create_container_btn.grid( 
            row = 7,
            column = 0,
            columnspan = 2,
            sticky = 'e' ,
            pady = ( 10 , 0 ),
            padx = ( 10, 20 ),
        )

##### Right Frame
        self.show_container_label = ctk.CTkLabel(
            self.right_frame,
            text = "Docker Container Information",
            font = ctk.CTkFont(
                family="Courier New",
                size=18,
                weight="bold",
                overstrike=False
            )
        )
        self.show_container_label.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            pady = ( 10, 0 ),
            padx = ( 60, 10 ),
            sticky = 'ew',
        )

# Container Management Table
        self.container_list = list( )
        headers =  [ "Select", "Name", "Status", "Netowrk", "IP Address" ]

        self.container_list.append( headers )
        
        # Extract data to a 2D array
        
        running_container = self.show_all_containers( )
        for i in range( 13 ) :
            self.container_list.append( [] )

        if running_container :
            for i, container in enumerate( running_container, 1 ) :
                self.container_list[i]= [ "▢", 
                                        container['name'], 
                                        "stopped" if container["status"].lower() == "exited" else container["status"],
                                        container["newtwork_name"],
                                        container["ip_addr"],
                                        ]

        self.container_table = CTkTable( 
                master = self.right_frame,
                values = self.container_list,
                width = 80,
                corner_radius = 3,
                command = self.on_table_click
        )

        self.container_table.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            padx= ( 30, 0 ),
            pady = ( 10, 0 ),
            sticky = "ew"
        )

        self.run_btn = ctk.CTkButton( 
            self.right_frame, 
            text="Run",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.run_container
        )
        self.run_btn.grid( 
            row = 2,
            column = 0,
            # columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 10 ),
        )

        self.stop_btn = ctk.CTkButton( 
            self.right_frame, 
            text="Stop",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.stop_container
        )
        self.stop_btn.grid( 
            row = 2,
            column = 1,
            # columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 10 ),
        )

        self.remove_btn = ctk.CTkButton( 
            self.right_frame, 
            text="Remove",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.remove_container
        )
        self.remove_btn.grid( 
            row = 3,
            column = 0,
            # columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 10 ),
        )

        self.refrash_btn = ctk.CTkButton( 
            self.right_frame, 
            text="Refresh",
            width = 130,
            height = 30,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.refrest_container_list,
        )
        self.refrash_btn.grid( 
            row = 3,
            column = 1,
            # columnspan = 2,
            sticky = 'e' ,
            pady = ( 35 , 0 ),
            padx = ( 10, 10 ),
        )

    def on_table_click( self, cell ) :
        row, column = cell["row"] , cell["column"]
        if row > 0 and column == 0:
            if self.container_list[row][0] == '▢' :
                self.container_list[row][0] = '🗹'
            else :
                self.container_list[row][0] = '▢'
            self.container_table.update_values( self.container_list )

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
        running_list = list()
        stoped_list = list()
        result = ''
        for row_idx, row in enumerate( self.container_list[1:], 1 ):
            if len(row) > 1 and row[0] == '🗹' and row[2] == "running" :
                running_list.append( row[1] )


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
                    CTkMessagebox(
                        title = "Success",
                        message = result,
                        icon = "check",
                        option_1 = "OK"
                    )
                    self.refrest_container_list( )
                else :
                    continue
            

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
                    result += f"The Container {i} is removed!!!\n"
                    CTkMessagebox(
                        title = "Success",
                        message = result,
                        icon = "check",
                        option_1 = "OK"
                    )
                    self.refrest_container_list( )
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
        headers =  [ "Select", "Name", "Status", "Netowrk", "ip_addr" ]
        self.container_list.append( headers )
        running_container = self.show_all_containers( )
        if running_container :
            for container in running_container :
                self.container_list.append( [ "▢", 
                                            container['name'], 
                                            "stopped" if container["status"].lower() == "exited" else container["status"],
                                            container["newtwork_name"],
                                            container["ip_addr"],
                                            ] )

        self.container_table.update_values( self.container_list )
