## Installation
- Clone the code
- (Recommended but not required) Create python venv `python -m venv /path/to/new/virtual/environment`
- Execute `pip install -r requirements`
- Create a `.env` file

### .env example:
```sh
LOG_LEVEL = "INFO" # TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
IPS_TO_CHECK = "192.168.0.2;192.168.0.3" # Separate by semicolon
PING_INTERVAL_SEC = 10
PING_TIMEOUT_SEC = 3
WEBHOOK_URL = "https://discord.com/api/webhooks/12345/ABC-DEF"
```
