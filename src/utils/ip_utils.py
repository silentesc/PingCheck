import socket
import subprocess
import platform
from loguru import logger

from src import env


class IpUtils:
    @staticmethod
    def is_ip_valid(ip: str) -> bool:
        """
        Checks if ip is valid format
        Args:
            ip (str): The ip to check
        Returns:
            bool: True if the ip format is valid, False otherwise
        """
        try:
            socket.inet_aton(ip) # Trys to convert IPv4 address to 32-bit packed binary format
            return True
        except socket.error:
            return False

    
    @staticmethod
    def ping_host(ip: str) -> bool:
        """
        Pings a host to check for connectivity
        Args:
            ip (str): The ip to check
        Returns:
            bool: True if the host is reachable, False otherwise
        """

        match (platform.system().lower()):
            case "windows":
                command = ["ping", "-n", "1", "-w", f"{env.get_ping_timeout_sec()}000", ip]
            case _:
                command = ["ping", "-c", "1", "-W", env.get_ping_timeout_sec(), ip]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
            logger.trace(f"Ping to {ip} successful")
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error running ping: {e}")
            return False
