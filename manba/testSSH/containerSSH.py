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
    def __init__( self, ssh_keys_dir)