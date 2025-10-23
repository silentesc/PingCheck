import threading
import time
from loguru import logger

from src.utils.ip_utils import IpUtils
from src.utils.discord_webhook_utils import DiscordWebhookUtils, EmbedColor
from src import env


def start_monitor(ip: str) -> None:
    logger.info(f"Monitoring for {ip!r} has been started")
    is_reachable: bool = True
    while True:
        start: float = time.monotonic()
        is_ping_success = IpUtils.hybrid_check(ip)
        if is_ping_success != is_reachable:
            is_reachable = is_ping_success
            if is_ping_success:
                logger.info(f"Host with IP `{ip}` is back online!")
                DiscordWebhookUtils.send_webhook_embed(EmbedColor.GREEN, "Host online", description=f"Host with IP `{ip}` is back online!")
            else:
                logger.info(f"Host with IP `{ip}` is offline!")
                DiscordWebhookUtils.send_webhook_embed(EmbedColor.RED, "Host offline", description=f"Host with IP `{ip}` is offline!")
        elapsed_sec: float = time.monotonic() - start
        remaining_sec: float = int(env.get_ping_interval_sec()) - elapsed_sec
        if remaining_sec > 0:
            logger.trace(f"Sleeping for remaining {remaining_sec} seconds")
            time.sleep(remaining_sec)
        else:
            time.sleep(1)


def main() -> int:
    for ip in set(env.get_ips_to_check().split(";")):
        if not IpUtils.is_ip_valid(ip):
            logger.error(f"IP {ip!r} is not valid IPv4 format, ignoring")
            continue
        t = threading.Thread(target=start_monitor, args=(ip,), daemon=True)
        t.start()

    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print()
            logger.info("Monitoring stopped by user")
            break

    return 0
