import logging
import requests
from requests.exceptions import HTTPError
from time import sleep


def xivapi_request(request_url):
    attempt = 0
    while True:
        try:
            response = requests.get(request_url)
            response.raise_for_status()
            json_response = response.json()
            attempt += 1

        except HTTPError as http_err:
            if attempt <= 3:
                logging.warning(
                    f"HTTP error occurred during XIV API data request: {http_err}. Retrying {4 - attempt} more "
                    f"time(s)"
                )
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.critical(
                    f"Final HTTP error occurred during FC data request: {http_err}. Failed XIV API Request "
                )
        except Exception as err:
            if attempt <= 3:
                logging.warning(
                    f"Other error occurred: {err}. Retrying {4 - attempt} more time(s)"
                )
                sleep(attempt)
                continue
            else:
                logging.error(f"Other error occurred: {err}. Failed XIV API request")
                exit()
        break
    return json_response
