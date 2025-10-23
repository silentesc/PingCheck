import socket
import subprocess
import platform
import time
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
    def tcp_check(ip: str, port: int = 22) -> bool:
        """
        Trys to create tcp connection to a host on port to check for connectivity
        Args:
            ip (str): The ip to check
        Returns:
            bool: True if the host is reachable, False otherwise
        """
        try:
            with socket.create_connection(address=(ip, port), timeout=int(env.get_ping_timeout_sec())):
                logger.trace(f"TCP check to {ip}:{port} successful")
                return True
        except ConnectionRefusedError:
            logger.trace(f"TCP check to {ip}:{port} successful")
            return True
        except OSError:
            logger.trace(f"TCP check to {ip}:{port} failed")
            return False


    @staticmethod
    def ping_check(ip: str) -> bool:
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
            success = result.returncode == 0
            logger.trace(f"Ping to {ip} {"successful" if success else "failed"}")
            return success
        except Exception as e:
            logger.error(f"Error running ping: {e}")
            return False


    @staticmethod
    def hybrid_check(ip: str) -> bool:
        """
        Trys to connect using the ping check (ICMP) first. When it fails it trys to connect via tcp.
        Args:
            ip (str): The ip to check
        Returns:
            bool: True if the host is reachable, False otherwise
        """
        if IpUtils.ping_check(ip):
            return True
        time.sleep(2) # Due to "No route to host" instead of timeout failure when instantly trying
        return IpUtils.tcp_check(ip)
