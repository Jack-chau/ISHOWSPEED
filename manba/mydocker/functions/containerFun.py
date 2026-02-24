import docker
import subprocess
class DockerContainerFun :
	def __init__( self ):
		try :
			self.client = docker.from_env( )
		except :
			print( 'Fail to initialize Docker client')

	def docker_ps( self ):
		result = ''
		try: 
			docker_ps = subprocess.run( 
				[ 'docker', 'ps' ],
				capture_output = True,
				text = True,
			)
			result += docker_ps.stdout
			return result
		except Exception as e :
			return( e )

	def docker_ps_all( self ):
		result = ''
		try: 
			docker_ps = subprocess.run( 
				[ 'docker', 'ps','-a' ],
				capture_output = True,
				text = True,
			)
			result += docker_ps.stdout
			return resultdoc
		except Exception as e :
			return( e )

	def new_container( self, 
					   name  = None, 
					   image = None, 
					   detach = True,
					   network = None, 
					   static_ip = None,
					   **kwargs
					) :

		image_defaults = {
            'ubuntu': '/bin/bash -c "while true; do sleep 1; done"',
            'centos': '/bin/bash -c "while true; do sleep 1; done"',
            'alpine': '/bin/sh -c "while true; do sleep 1; done"',
            'debian': '/bin/bash -c "while true; do sleep 1; done"'
        }

		base_image = image.split(':')[0].lower()

		if base_image in image_defaults:
			command = image_defaults[base_image]
		else :
			command = None

		port = kwargs.pop('ports', dict( ) )

		if port :
			host_port, container_port = port.split( ':' )
			port = { f"{container_port}/tcp" : int( host_port ) }

		try :
			container = self.client.containers.run( 
				name = name,
				image = image,
				detach = detach,
				command = command,
				ports = port,
			)

			if static_ip and network:
				docker_network = self.client.networks.get( network )
				docker_network.connect( container, ipv4_address = static_ip )

			if network != 'bridge' :
				docker_network = self.client.networks.get( "bridge" )
				docker_network.disconnect( container )

			container.reload( )

			result = ''

			if detach :
				result += ( f"container {container.id} is running with detach mode\n" )
			else :
				result += ( f"container {container.id} is running without detach mode\n" )

			result += self.docker_ps( )

			return result

		except Exception as e :
			return( e )

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



	def remove_container( self ) :
		all_containers = self.client.containers.list(all=True)
		for container in all_containers:
			container.stop()
			container.remove()
			(f"Removed exited container: {container.name}")
a = DockerContainerFun()
