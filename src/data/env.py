import os
import dotenv
from loguru import logger


class Env:
    def __init__(self) -> None:
        logger.debug("Loading env")
        dotenv.load_dotenv()


    def __get_var(self, var_name: str) -> str:
        env: str | None = os.getenv(var_name)
        if env is None:
            raise ValueError(f"Environment variable '{var_name}' is not set.")
        return env


    def get_log_level(self) -> str:
        return self.__get_var("LOG_LEVEL")


    def get_ips_to_check(self) -> str:
        return self.__get_var("IPS_TO_CHECK")


    def get_ping_interval_sec(self) -> str:
        return self.__get_var("PING_INTERVAL_SEC")


    def get_ping_timeout_sec(self) -> str:
        return self.__get_var("PING_TIMEOUT_SEC")


    def get_webhook_url(self) -> str:
        return self.__get_var("WEBHOOK_URL")


ENV = Env()
