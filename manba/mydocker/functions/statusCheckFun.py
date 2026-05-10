import docker
import subprocess

class DockerSCFun( ) :
	def __init__( self ):
		self.client = docker.from_env( )
# Ping
	def check_connection( self ) :
		try :
			self.client.ping( )
			welcome = rf"""
					         🫧
					   🫧🫧🫧🫧          
					 🫧🫧🫧🫧🫧🫧     
					🫧🫧🫧🫧🫧🫧🫧🫧
					##########"\___/ ===
					{{    /  ====	\_____/ 
					 \____ o         __/
					  \    \        ___/
					   \    \     ___/
					    \____\___/

					DOCKER: 🐳Yea!!!🐳
			    🔥🔥🔥Docker are successfully connected!🔥🔥🔥
			"""
			return welcome
			# self.docker_gui.docker_textbox.insert( 'end', welcome )
		except Exception as e :
			return ( f"❌Failed to connect to Docker: {str( e ) }❌" )
		
# Check docker client version
	def check_docker_client_version( self ) :
		client_ver = docker.__version__
		return( f"The docker client version is: { client_ver }\n" )

# Check docker server version
	def check_docker_server_version( self ) :
		server_ver = self.client.version( )
		return( f"The docker server version is: {server_ver[ "Version" ]}\n" )

# Check docker context
	def show_docker_contexts( self ) :
		try :
			result = subprocess.run( 
										[ 'docker', 'context', 'ls' ], 
										capture_output = True, 
										text = True, 
										check = True 
									)
			lines = result.stdout.splitlines()
			formatted_output = ""

			if lines :
				headers = lines[0].split()
				formatted_output = f"{headers[0]:<20} {headers[1]:<25} {headers[3]}\n"
				formatted_output += "-" * 150 + "\n"

				for line in lines[1:2]:
					if line.strip( ):
						parts = line.split( )
						formatted_output += f"{parts[0]} {parts[1]:<13} {parts[3]:<23} {' '.join(parts[6:])}\n"
				for line in lines[2:]:	
					if line.strip( ):
						parts = line.split( )
						formatted_output += f"{parts[0]:<17} {parts[1]} {parts[2]:<18} {' '.join(parts[3:])}\n"
					
			return formatted_output

		except subprocess.CalledProcessError as e :
			return( f"Error executing command: {e}\nError output: {e.stderr}" )

# Check docker info in detail
	def show_docker_info( self ) :
		try :
			result = subprocess.run( 
										[ 'docker', 'info' ], 
										capture_output = True, 
										text = True, 
										check = True 
									)
			return( result.stdout )
		except subprocess.CalledProcessError as e :
			return( f"Error executing command: {e}\nError output: {e.stderr}" )

# Check docker network
	def show_network_contexts( self ) :
		try :
			result = subprocess.run( 
				[ 'docker', 'network', 'ls' ], 
				capture_output = True, 
				text = True, 
				check = True 
			)
			
			lines = result.stdout.strip().split( '\n' )
			formatted_output = ''

			if lines :
				headers = lines[0].split( )
				formatted_output = f"{headers[0]} {headers[1]:<17} {headers[2]:<35} {headers[3]}\n"
				formatted_output += "-" * 150 + '\n'
				
				for line in lines[1:2]:
					if line.strip( ) :
						parts = line.split( )
						formatted_output += f"{parts[0]:<24} {parts[1]:<37} {parts[2]} \n"

				for line in lines[2:3]:
					if line.strip( ):
						parts = line.split()
						formatted_output += f"{parts[0]:<25} {parts[1]:<38} {parts[2]} \n"
				
				for line in lines[3:4]:
					if line.strip( ):
						parts = line.split()
						formatted_output += f"{parts[0]:<25} {parts[1]:<27} {parts[2]} \n"

				for line in lines[4:]:
					if line.strip( ):
						parts = line.split()
						formatted_output += f"{parts[0]:<24} {parts[1]:<37} {parts[2]} \n"

			return( formatted_output )
		except subprocess.CalledProcessError as e :
			return( f"Error executing command: {e}\nError output: {e.stderr}" )

# Show all containers
	def show_all_containers( self ) :
		containers = self.client.containers.list( all = all )
		containers_list = list( )
		# network_info = dict()
		for container in containers :
			network_settings = container.attrs['NetworkSettings']['Networks']
			containers_list.append(
				{
					'id' : container.short_id,
					'name' : container.name,
					'status' : container.status,
					'newtwork_name' : list( container.attrs['NetworkSettings']['Networks'].keys())[0],
					'network_type' : container.attrs['NetworkSettings']['Networks'][network_name]['driver'],
					'ip_addr' : container.attrs['NetworkSettings']['IPAddress'],
					'port' : container.attrs['NetworkSettings']['Ports']
				}
			)
		if len( containers_list ) > 0 :
			return containers_list
		else :
			return( "No running container" )

# Show running containers
	def show_runing_containers( self ) :
		running_containers = self.client.containers.list( all = False )
		running_containers_list = list( )
		for container in running_containers :
			network_settings = container.attrs['NetworkSettings']['Networks']
			# Get network if exists
			if network_settings :
				network_info = dict()
				for network_name, network_setting in network_settings.items( ) :
					network = self.client.networks.get( network_setting[ 'NetworkID' ] )
					network_info[network_name] = {
						'driver' : network.attrs['Driver'],
						'network_id' : network.id,
						'ip_address' : network_setting['IPAddress'],
					}

			running_containers_list.append(
				{
					'id' : container.short_id,
					'name' : container.name,
					'status' : container.status,
					'newtwork_name' : list( network_info.keys())[0],
					'network_type' : network_info[network_name]['driver'],
					'ip_addr' : network_info[network_name]['ip_address'] ,
					'ports' : ', '.join( container.attrs['NetworkSettings']['Ports'].keys() )
				}
			)
		if len( running_containers_list ) > 0 :
				result = self.show_container_info( running_containers_list )
				return( result )
		else :
			return( "No running containers" )


	def show_container_info( self, data_list ) :
		id = True
		name = True
		status = True
		network_type = True
		newtwork_name = True
		ip_addr = True
		port = True
		num_of_container = 0
		result = ''

		for i in data_list:
			if i['id'] and id == True :
				keys = f"{'Container ID':<20}"
				values = f"{i['id']:<16}"

			if i['name'] and name == True :
				keys += f"{'Name':<18}"
				values += f"{i['name']:<17}"

			if i['status'] and status == True :
				keys += f"{'Status':<15}" 
				values += f"{i['status']:<13}"
				
			if i['newtwork_name'] and newtwork_name == True :
				keys += f"{'Newtwork Name':<20}" 
				values += f"{i['newtwork_name']:<27}" 

			if i['network_type'] and network_type == True :
				keys += f"{'Network Type':<20}" 
				values += f"{i['network_type']:<17}"

			if i['ip_addr'] and ip_addr == True :
				keys += f"{'IP addr':<20}" 
				values += f"{i['ip_addr']:<18}" 

			if i['ports'] and port == True :
				keys += f"{'Port':<20}" 
				values += f"{i['ports']:<18}" 

			num_of_container += 1
			result += f"The NO:{str(num_of_container)} container status:\n{keys}\n{values}\n"

		return( result)

# Container Inspect
	def inspect_container( self, target_container ) :
		try :
			target_container = self.client.containers.get( target_container )
			container_attrs = target_container.attrs
			result = ( f"Container Name: { target_container.name }\n" )
			result += ( f"Container ID: { target_container.id }\n" )

			result += ( f"Status: { target_container.status }\n" )
			result += ( f"Image: { target_container.image.tags }\n" )
			result += ( f"Time Created: { target_container.attrs[ "Created" ] }\n" )

			result += ( "\nNetwork Settings:" )
			networks = target_container.attrs[ 'NetworkSettings' ][ 'Networks' ]
			port = target_container.attrs[ 'NetworkSettings' ][ 'Ports' ]
			if port : 
				for net_name, net_config in networks.items( ) :
					result += ( f"\t\tNetwork: { net_name }\n" )
					result += ( f"\t\tIP Address: {net_config["IPAddress"]}\n")
					result += ( f"\t\tPorts: { ', '.join( port.keys())}\n" )
				return result
			else :
				for net_name, net_config in networks.items( ) :
					result += ( f"\t\tNetwork: { net_name }\n" )
					result += ( f"\t\tIP Address: {net_config["IPAddress"]}\n" )
					return result
		except:
			return (f"Container {target_container} not found\n")

	def inspect_network( self, target_network ) :
		try :
			network = self.client.networks.get( target_network )
			result = '';
			output = {
				"Name" : network.name,
				"ID" : network.id,
				"Driver" : network.attrs[ 'Driver' ],
				"Subment" : network.attrs['IPAM']['Config'][0]['Subnet'],
				"Gateway" : network.attrs['IPAM']['Config'][0]['Gateway'],
				"Created" : network.attrs['Created'],
			}
			
			for key, value in output.items( ):
				result += ( f"{key:5}: {value}\n" )
			return result

		except docker.errors.NotFound :
			return f"Network {target_network} not found."
		except Exception as e :
			return f"Error: {str(e)}"