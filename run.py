import sys
import os
from loguru import logger


if __name__ == "__main__":
    from src import main, env

    log_level = env.get_log_level() or "INFO"
    if log_level == "TRACE":
        log_format = "[{time:YYYY-MM-DD HH:mm:ss}] [<level>{level}</level>] [{file}:{function}:{line}]: {message}"
    else:
        log_format = "[{time:YYYY-MM-DD HH:mm:ss}] [<level>{level}</level>]: {message}"

    logger.remove(0)
    logger.add(
        sys.stdout,
        level=log_level,
        format=log_format,
        colorize=True,
        backtrace=True,
        diagnose=False
    )

    sys.exit(main.main())
