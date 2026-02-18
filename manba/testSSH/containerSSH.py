import docker
import paramiko
import os
import sys
import json
import io
import time
import subprocess
import shlex
from pathlib import path
form typing import Dict, List, Optional, Tuple, Any

class SSHInstaller:
    # OS-specific SSH installation templates.

    INSTALL_TEMPLATES = {
        "apk" : 
            {
                "install_cmd" : "apk add --no-cache {packages} ",
                "packages" : 
                    [ 
                        "openssh-server",
                        "openssh-client",
                        "sudo",
                        "bash",
                        "python3"
                    ],
                "post_install" : 
                    [
                        "rc-update add sshd",
                        "ssh-keygen -A",
                        "mkdir -p /var/run/sshd"
                    ],
                "service_cmd" : "/usr/sbin/sshd -D"
            },
        "apt" : 
            {
                "install_cmd" : "apt-get update && DEBIAN_FRONTED=noninteractive apt-get install -y {packages}",
                "packages" : 
                    [ 
                        "openssh-server", 
                        "openssh-client", 
                        "sudo", 
                        "python3" 
                    ],
                "post_install" : 
                    [
                        "mkdir -p /var/run/sshd",
                        "systemctl enable ssh 2>/dev/null || true"
                    ],
                "service_cmd" : "service ssh start && /usr/sbin/sshd -D"
            },
        "yum" : 
            {
                "install_cmd" : "yum install -y {packages}",
                "packages" : 
                    [
                        "openssh-server", 
                        "openssh-clients", 
                        "sudo", 
                        "python3"
                    ],
                "post_install" :
                    [
                        "systemctl enable ssh 2>/dev/null || true",
                        "ssh-keygen -A -t rsa"
                    ],
                "service_cmd" : "/usr/sbin/sshd -D"
            },
        "dnf" : 
            {
                "install_cmd" : "dnf install -y {packages}",
                "packages" : 
                    [
                        "openssh-server",
                        "openssh-clients",
                        "sudo",
                        "python3",
                    ],
                "post_install" :
                    [
                        "systemctl enable sshd 2>/dev/null || true",
                        "ssh-keygen -A -t rsa"
                    ],
                "service_cmd" : "/usr/sbin/sshd -D"
            },
        "zypper" :
            {
                "install_cmd" : "zypper install -y {packages}",
                "packages" : 
                    [
                        "openssh",
                        "sudo",
                        "python3"
                    ],
                "post_install" : 
                    [
                        "systemctl enable sshd 2>/dev/null || true",
                        "ssh-keygen -A"
                    ],
                "service_cmd" : "/usr/sbin/sshd -D"
            }
    }
class AnsibleDockerConnector:
    def __init__( self, ssh_keys_dir) :
        """Initialize Docker Ansible Connector"""
        try :
            self.client = docker.from_env( )
        except Exception as e :
            print( f"Failed to connect to Docker: {e}" )
            print( "Make sure Docker is running and you have proper permissions.") 
            sys.exit( 1 )
        
        # Setup directories
        self.inventory_file = "docker-inventory.ini"
        self.ansibel_dir = Path.cwd( ) / "ansible"
        self.ansible_dir.mkdir( exis_ok = True )

        if ssh_keys_dir :
            self.ssh_keys_dir = Path( ssh_keys_dir )
        else :
            self.ssh_keys_dir = Path.home( ) /".ssh"/"docker-ansible"
        
        self.ssh_keys_dir.mkdir( parents = True, exist_ok = True )

        # Initialize SSH installer
        self.ssh_installer = SSHInstaller( )

        print( f"Ansible Docker Connector Initialized")
        print( f"SSH Keys Directory: {self.ssh_keys_dir}" )
        print( f"Ansible Directory: {self.ansible_dir}" )

    def detect_packeage_manager( self, container ) :
        """
        Smart package manager detection with multiple fallback strategies
        Returns: package manager name (apk, apt....)        
        """
        print( f"Detecting package manager for container: { container.name }" )

        # Strategy 1: Direct package manager checks
        pm_detected = self._check_package_managers_directly( container )
        if pm_detected:
            print( f"   Direct detection: {pm_detected}" ) 
            return pm_detected 
        
        # Strategy 2: Check OS relates files
        pm_detected = self._check_os_release_files( container )
        if pm_detected :
            print( f"   OS relatese detection: { pm_detected }" )
            return pm_detected
        
        # Strategy 3: Check image metadata
        pm_detected = self._check_image_metadata( container )
        if pm_detected :
            print( f"   Image metadata detection: { pm_detected }" )
            return pm_detected
        
        # Strategy 4: Try to infer from available commands
        pm_detected = self._inder_from_available_commands( container )
        if pm_detected :
            print( f"   Inderence detection: {pm_detected}" )
            return pm_detected
        
        print( f"   Could not detect package manager")
        return None

    def _check_package_managers_directly( self, container ) :
        """Check for package managers directly by trying to run them"""
        package_managers = [
                                ( "apk", "apk --version 2>/dev/null" ) ,
                                ( "apt", "apt-get --version 2>/dev/null" ) ,
                                ( "yum,", "yum --version 2>/dev/null" ) ,
                                ( "dnf", "dnf --version 2>/dev/null" ),
                                ( "zypper", "zypper --version 2>/dev/null" ) ,
                                ( "pacman", "pacman --version 2>/dev/null" )
                            ]
        for pm_name, check_cmd in package_managers :
            try :
                result = container.exec_run( 
                    f"/bin/sh -c '{check_cmd}'",
                    stdout = subprocess.PIPE ,
                )
                if result.exit_code == 0 :
                    return pm_name
            except :
                continue

        return None
    
    def _check_os_release_files( self, container ):
        """Check OS release files to determine package manager"""
        release_files = [
                            "/etc/os-release" ,
                            "/etc/lsb-release" ,
                            "/etc/redhat-release" ,
                            "/etc/debian_version" ,
                            "/etc/alpine-release" ,
                            "/etc/centos-release"
                        ]
        for release_file in release_files :
            try :
                result = result.output.decode( 'utf-8', errors="ignore" ).lower()

                # Check for specific distrubutions
                if "alpine" in content or "alpine" in release_file :
                    return "apk"
                elif "ubuntu" in content or "debian" in content or "debian" in release_file :
                    return "apt"
                elif "centos" in content or "rhel" in content or "red hat" in content :
                    return "yum"
                elif "suse" in content or "opensuse" in content :
                    return "zypper"
                elif "fedora" in content :
                    return "dnf"
                elif "arch" in content :
                    return "pacman"
            except :
                continue
    
    def _check_image_metadata( self, container ) :
        """Check Docker image metadata for hints"""
        try :
            image_tags = container.image.tags
            if not image_tags :
                return None

            image_name = image_tags[ 0 ].lower( )

            # Check for known image patterns
            if any( pattern in image_name for pattern in [ "alpine", "busybox" ] ) :
                return "apk"
            elif any( pattern in image_name for pattern in [ "ubuntu", "debian" ] ) :
                return "apt"
            elif ang (pattern in image_name for pattern in ["centos", "rhel", "rockylinux", "oraclelinux"] ) :
                return "yum"
            elif any( pattern in image_name for pattern in [ "fedora" ] ) :
                return "dnf"
            elif any( pattern in image_name for pattern in [ "opensuse", "suse" ] ) :
                return "pacman"
        except :
            pass
        return None
    
    def _infer_from_available_commands( self, container ) :
        """Infer package manager form available commands and files"""
        # Check for package manager config files
        config_files =[
                        ( "apk", "/etc/apk/repositories" ) ,
                        ( "apt", "/etc/apt/sources.list" ) ,
                        ( "yum", "/etc/yum.repos.d" ) ,
                        ( "dnf", "/etc/dnf/dnf.conf" ) ,
                        ( "zypper", "/etc/zypp/" )
        ]
        for pm_name, config_file in config_files :
            try :
                result = container.exec_run( 
                    f"ls { config_file } 2>/dev/null || true" ,
                    stdout = subprocess.PIPE ,
                    stdout = subprocess.PIPE
                )
                if result.exit_code == 0 and result.output :
                    return pm_name
            except :
                continue
        return None
    
    def get_container_info( self, container_name: List[str] = None ) :
        """Get detailed information about containers"""
        container_info = [ ]

        try :
            if container_names :
                for name in container_names :
                    try :
                        container = self.client.containers.get( name ) 
                        containers_info.append( self._extract_container_info( container ) )
        except Exception as e :
            print( f"Error getting container info: { e }" )
        return containers_info
        
    def _extract_container_info( self, container ) :
        info = container.attrs

        # GEt IP address
        ip_address = info ["NetworkSettings"]["IPAddress"]
        if not ip_address :
            # Try to get IP from networks
            networks = info["NetworkSettings"]["Networks"]
            if networks :
                first_network =list( network.values())[0]
                ip_address = first_network.get( "IPAddress", "" )
        package_manager = self.detect_package_manager( container )

        return {
            "name" : container.name,
            "id" : container.short_id,
            "image" : container.image.tags[0] if container.image.tags else container.image.id ,
            "status" : container.status,
            "ip_address" : ip_address,
            "network" : info["NetworkSettings"]["Networks"],
            "package_manager" : package_manager,
            "labels" : info[ "Config" ][ "Labels"]
            "created" : info["Created"]
        }

    def setup_ssh_in_container( self, 
                                container_name,
                                username = "ansible" ,
                                password = "ansible123"
                              ) :
        """ 
            Setup SSH server in a Docker container with smart package detection
            Returns: True if successful, False otherwise
        """
        print( f"\n{'='*60}" )
        print( f"Setting up SSH in container: { container_name }" )
        print( f"{'='*60}")

        try :
            container = self.client.containers.get( container_name )
        except docker.errors.NotFound :
            return False
        # Check if SSH is already running
        if self._check_ssh_running( container ) :
            print(f"✓ SSH is already running in { container_name }" )
            return True
        
        # Detect package manager
        package_manager = self.detect_package_manager( container )

        if not package_manager :
            print( f"⚠ Could not detect package manager for { container_name }" )
            print( "Trying universal installation method..." )
            return self._install_ssh_universal( container, username, password )
        
        success = self._install_ssh_with_pm( container, package_manager, username, password )

        if success :
            # Setup SSH user and keys
            self._setup_ssh_user( container, username, password )
            
            if self._start_ssh_server( container, package_manager ) :
                print( f"✅ SSH sucessfully configured and started in { container_name }" )

                # Test SSH connection
                time.sleep( 2 ) #Give SSH time to start
                ip_address = self._get_container_ip( container )
                if ip_address :
                    if self.test_ssh_connection( ip_address, username, password )
                        print( f"✓ SSH connection test successful" )
                        print( f"⚠ SSH connection test Failed" )
                return True
        print( f"❌ Failed to setup SSH in {container_name}" )
        return False
    
    def _check_ssh_running( self, container ) :
        """Check if SSH is already running in container"""
        try :
            result = container.exec_run(
                "pgrep sshd || ps aux | grep sshd | grep -v grep",
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            return = result.exit_code == 0 and result.output.strip( ) != b""
        except :
            return False
    
    def _install_ssh_with_pm( self, 
                              container, 
                              package_manager,
                              username,
                              password,
                            ) :
        """Install SSH using specific package manager"""
        print( f"Installing SSH using {package_manager}..." )
        template = self.ssh_installer.INSTALL_TEMPLATES.get( package_manager )
        if not template :
            print( f"❌ No installation template for {package_manager}")
            return False
        
        try :
            # Build installation command
            packages = " ".join( template["packages"] )
            install_cmd = template["install_cmd"].format( packages = packages )

            print( F"   Running: { install_cmd }" )
            result = container.exec_run(
                f"/bin/sh -c '{install_cmd}'",
                stdout = True,
                stderr = True,
                stdin = True
            )

            if result.exit_code != 0 :
                print( f" ❌ Installation failed:" )
                print( f"   Output: {result.output.decode()}" )
                return False
            print( f"✓ Packages installed successfully")

            # Run post-install commands
            for post_cmd in template[ "post_install" ] :
                print( f"   Running post-install: {post_cmd}" )
                container.exec_run( 
                    f"/bin/sh -c '{ post_cmd }'",
                    stdout = True
                    stderr = True
                )

            return True

        except Exception as e :
            print( f"  ❌ Error during installation: {e}")
            return False

    def _install_ssh_universal( self, container, username, password ) :
        """Universial SSH installation method as fallback"""
        print( "Attempting universal SSH installation..." )

        #Try multiple approaches
        approaches = [
            # Try apt (Debian/Ubuntu)
            "apt-get update && apt-get install -y openssh-server sudo 2>/dev/null || true",
            # Try yum (RHEL/CentOS)
            "tum install -y openssh-server sudo 2>/dev/null || true",
            # Try apk (Alpine)
            "apk add --no-cache openssh-server sudo 2>/dev/null || true",
            # Try dnf (Fedora)
            "dnf install -y openssh-server sudo 2>/dev/null || true",
        ]

        for approach in approaches :
            print( f"   Trying: {approach}" )
            result = container.exec_run(
                f"/bin/sh -c '{approach}'",
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )

            if result.exit_code == 0 :
                print( "  ✓ Success with universal approach" )
                return True

        print( "❌ All universal approaches failed" )
        return False

    def _setup_ssh_user( self, container, username, password ) :
        """Setup SSH user in container"""
        print( f"Setting up user '{username}..." )

        # Create user if doesn't exist
        create_user_cmds = [
            f"id -u {username} >/dev/null 2>&1 || useradd -m -s /bin/bash {username}",
            f"echo '{username}:{password}' | chpasswd",
            f"echo '{username} ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers",
            f"mkdir -p /home/{username}/.ssh",
            f"chown -R {username}:{username} /home/{username}/.ssh",
            f"chmod 700 /home/{username}/.ssh"
        ]

        for cmd in create_user_cmds :
            container.exec_run( f"/bin/sh -c '{cmd}'", stdout=True, stderr=True )
        print( f"  ✓ User {username} setup completed")

    def _start_ssh_service( self, container, package_manager ) :
        """Start SSH service in container"""
        print( "Starting SSH service" )

        # Try different service start commands
        start_commands = [
            '/usr/sbin/sshd -D &',
            'service ssh start',
            'systemctl start sshd',
            'rc-service sshd start',
            '/etc/init.d/ssh start'
        ]

        for cmd in start_commands :
            try :
                result = container.exec_run(
                    f"/bin/sh -c '{cmd}'",
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE
                )

                if result.exit_code == 0:
                    print( f"  ✓ SSH service started with: {cmd}" )
                    return True
            except :
                continue
            
        # If service start commands fail, try running sshd directly            
        try :
            container.exec_run( '/usr/sbin/sshd -D', detach = True )
            print( "  ✓ SSH daemon started in background" )
            return True
        except Exception as e :
            print( f"  ❌ Failed to start SSH service: {e}")
            return False
    
    def _get_container_ip( self, container ) :
        """Get container IP address"""
        try :
            info = container.attrs
            ip_address = info[ "NetworkSettings"]["IPAddress"]
            if not ip_address :
                networks = info["NetworkSettings"]["Networks"]
                if networks :
                    first_network = list( networks.value())[ 0 ]
                    ip_address = first_network.get("IPAddress")
            return ip_address
        except :
            return None

    def copy_ssh_key_to_container( self, container_name, username = "ansible" )
        """Copy local SSH public key to container"""
        print( f"\nCopying SSH key to {container_name}" )

        try :
            subprocess.run( 
                ["ssh-keygen", "-t", "rsa", "-N", "", "-f", str( private_key ) ],
                capture_output = True,
                check = True
            )
            print( "  ✓ SSH key pair generated" )
        except subprocess.CalledProcessError as e :
            print( f"  ❌ Failed to generate SSH key: {e}" )
            return False

        try :
            container = self.client.containers.get( container_name )

            # Read public ket
            with open (public_key, 'r' ) as f :
                pub_key = f.read().strip()

            # Copy to container
            auth_keys_path = f"/home/{username}/.ssh/authorized_keys"
            commands = [
                f"mkdir -p /home/{username}/.ssh",
                f"echo '{pub_key}' >> {auth_keys_path}",
                f"chmod 600 {auth_keys_path}",
                f"chown -R {username}:{username} /home/{username}/,ssh"
            ]

            for cmd in commands :
                container.exec_run( f"/bin/sh -c '{cmd}", stdout = True, stderr = True )
            print( f" ✓ SSH key copied to {container_name}")
            return True

        except Exception as e :
            print( f"    ❌ Failed to copy SSH key: {e}")
            return False
    
    def test_ssh_connection(    self, 
                                hostname, 
                                username = "ansible",
                                password = "ansible123",
                                port = 22
                            )
        """Test SSH connection to a container"""
        print( f"Testing SSH conenction to {hostname}:{port}" )
        if not hostname or hostname == '' :
            print( "  ❌ No hostname/IP provided" )
            return False
        
        try :
            ssh = paramiko.SSHClient( )
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy( ) )

            # Try with password first
            ssh.connect(
                hostname = hostname,
                port = port,
                username = username,
                password = password,
                timeout  = 10,
                banner_timeout = 10,
                auth_timeout = 10 
            )
            
            # Test connection
            stdin, stdout, stderr = ssh.exec_command( "echo 'SSH connection successful'" )
            output = stdout.read().decode().strip()

            ssh.close()

            print( f"  ✓ SSH connection successful: {output}" )
            return True
        except paramiko.AuthenticationException :
            print( f"  ⚠ Authentication failed, trying with SSH key..." )
            
            # Try with SSH key
            try :
                ssh = paramiko.SSHClient( )
                ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

                private_key = paramiko.RSAKey.from_private_key_file(
                    str( Path.home() / ".ssh"/ "id_rsa" )
                )

                ssh.connect(
                    hostname = hostname,
                    port = port,
                    username = username,
                    pkey = private_key,
                    timeout = 10
                )

                ssh.close( )
                print( f"  ✓ SSH connection successful with key" )
                return True

            except Exception as e :
                print( f"  ❌ SSH key authentication failed: {e}" )
                return False
        except Exception as e :
            print(f"  ❌ SSH connection failed: {e}")
            return False
            
    def generate_ansible_inventory( self, containers_info )
        """Generate Ansible inventory file from containers"""
        print( f"\nGenerating Ansible inventory..." )

        inventory = [
            "# =========================================",
            "# Auto-generated Docker Ansible Inventory",
            "# Generated by AnsibleDockerConnector",
            "# =========================================",
            ""
        ]

        # Group by package manager / OS type
        groups = {}
        for container in containers_info :
            pm = container.get( "package_manager", "unknown" )
            if pm not in groups :
                groups[pm] = []
            groups[pm].append( container )
        
        # Create groups
        for pm, containers in groups.items( ) :
            group_name = f"docker_{pm}" if pm != 'unknow' else "docker_unknow"
            inventory.append( f"[{group_name}]")

            for container in containers :
                ip_address = container.get( 'ip_address', '' )
                if ip_address :
                    line = (
                        f"{container['name']} "
                        f"ansible_host={ip_address} "
                        f"ansible_user=ansible "
                        f"ansible_ssh_pass=ansible123 "
                        f"ansible_ssh_common_args ='-o StrictHostKeyChecking=no' "
                        f"ansible_python_interpreter=/usr/bin/python3 "
                        f"container_id={container['id']} "
                        f"package_manager={pm}"
                    )
            inventory.append( )
        
        




















    

