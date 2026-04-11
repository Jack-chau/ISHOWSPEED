import docker
import subprocess

class DockerNetworkFun( ) :
	def __init__( self ):
		try :
			self.client = docker.from_env( )
		except :
			print( 'Fail to initialize Docker client')

	def list_networks( self ) :
		result = ''
		try :
			network_list = subprocess.run(
				[ 'docker', 'network', 'ls' ],
				capture_output = True,
				text = True,
				check = True,
			)
			result += network_list.stdout
			return result
		except Exception as e  :
			return e

	def create_network( self,
						name = None, 
						driver = "bridge",
						subnet = None,
						gateway = None,
						attachable = True,	
					) :
		try :
			output = ""
			if not name : 
				return f"Please Input the network name!\n"
			
			ipam_config = { "driver" : "default" }
			config = dict( )
			if subnet :
				config["subnet"] = str( subnet )
				if gateway :
					config["gateway"] = str( gateway )
			
			ipam_config["config"] = [ config ]

			network = self.client.networks.create(
							name = str( name ),
							driver = driver,
							attachable = attachable,
							ipam = ipam_config
						)
			if network :
				output += f"docker network name: {name} has been created.\n\n"
				output += self.list_networks( )
			else :
				output +=  "Failed to create network." 
				
			return output

		except docker.errors.APIError as e:
			return f"Failed to create network: {str(e)}\n"
		except Exception as e:
			return f"Unexpected error: {str(e)}\n"		

	def remove_network( self, name ) :
		try :
			network = self.client.networks.get( str( name ) )
			network.remove( )
			return f"network name '{name}' has been removed"
		except Exception as e:
			return f"Unexpected error: {str(e)}\n"	


	def set_static_ip(self, container_name, network_name, static_ip ):
		try :
		# Get container and network object in docker
			container = self.client.containers.get( container_name )
			target_network = self.client.networks.get( network_name )

			if not static_ip :
				return "Please enter static ip!!!"
			
			# Get current network connection status
			container.reload()
			connected_network = container.attrs["NetworkSettings"]["Networks"]

			# Disconnect from ALL current networks
			if not connected_network :
				pass
			else :
				for net_name in list( connected_network.keys() ) :
					if not net_name :
						continue
					try :
						net_obj = self.client.networks.get( net_name )
						net_obj.disconnect( container )
					except Exception :
						print(f"Skipping disconnect for {net_name}: {e}")


			# Assign static ip to container
			target_network.connect( container, ipv4_address = static_ip )

			container.reload()
			return f"Successfully set IP {static_ip} on network {network_name}"
			
		except Exception as e :
			return( str( e ) )
		
dnf = DockerNetworkFun()