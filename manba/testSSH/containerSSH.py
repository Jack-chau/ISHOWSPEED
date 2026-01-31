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
            self.ssh_keys_dir = Path.home( ) / ".ssh" / "docker-ansible"
        
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