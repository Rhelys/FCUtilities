import logging
import requests
from requests.exceptions import HTTPError
from time import sleep


def get_fc_info(fc_id):
    fc_request = (
        f"https://xivapi.com/freecompany/{fc_id}?columns=FreeCompany.ActiveMemberCount,"
        f"FreeCompany.ID,FreeCompany.Name,FreeCompany.Server,FreeCompany.Tag"
    )

    # Retrieving general FC information
    attempt = 1
    while True:
        try:
            fc_response = requests.get(fc_request)
            fc_response.raise_for_status()
            fc_data = fc_response.json()
        except HTTPError as http_err:
            if attempt <= 3:
                logging.warning(
                    f"HTTP error occurred during FC data request: {http_err}. Retrying {4 - attempt} more "
                    f"time(s)"
                )
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.critical(
                    f"Final HTTP error occurred during FC data request: {http_err}. Failed to get info "
                    f"for FC ID: {fc_id}"
                )
        except Exception as err:
            if attempt <= 3:
                logging.warning(
                    f"Other error occurred: {err}. Retrying {4 - attempt} more time(s)"
                )
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(
                    f"Other error occurred: {err}. Failed to get info for FC ID: {fc_id}"
                )
                exit()
        break
    return fc_data


def get_fc_members(fc_id):
    # Retrieving FC members list

    fc_member_request = (
        f"https://xivapi.com/freecompany/{fc_id}?data=FCM&columns=FreeCompanyMembers.*.ID,"
        f"FreeCompanyMembers.*.Name"
    )

    attempt = 1
    while True:
        try:
            fc_member_response = requests.get(fc_member_request)
            fc_member_response.raise_for_status()
            fc_member_list = fc_member_response.json()
        except HTTPError as http_err:
            if attempt <= 3:
                logging.warning(
                    f"HTTP error occurred: {http_err}. Retrying {4 - attempt} more time(s)"
                )
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(
                    f"HTTP error occurred: {http_err}. Failed to get members for FC ID: {fc_id}"
                )
        except Exception as err:
            if attempt <= 3:
                logging.warning(
                    f"Other error occurred: {err}. Retrying {4 - attempt} more time(s)"
                )
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(
                    f"Other error occurred: {err}. Failed to get members for FC ID: {fc_id}"
                )
                exit()
        break
    return fc_member_list


def character_output(character):
    # XIVAPI private keys allow for higher rate limits
    """if privatekey != "":
        requesturl = (
            f"https://xivapi.com/character/{character}?columns=Character.Name"
            f"&private_key={privatekey}"
        )
    else:"""

    requesturl = f"https://xivapi.com/character/{character}?columns=Character.Name"

    char_attempt = 1
    error_count = 0

    while True:
        try:
            response = requests.get(requesturl)
            response.raise_for_status()
            characteracjson = response.json()
        except HTTPError as char_http_err:
            if char_attempt <= 3:
                logging.info(
                    f"HTTP error occurred: {char_http_err}. Trying {4 - char_attempt} more time(s)"
                )
                char_attempt += 1
                sleep(char_attempt)
                continue
            else:
                logging.warning(
                    f"HTTP error occurred: {char_http_err}. Achievement request for {character} failed"
                )
                error_count += 1
                return
        except Exception as ac_err:
            if char_attempt <= 3:
                logging.info(
                    f"HTTP error occurred: {ac_err}. Trying {4 - char_attempt} more time(s)"
                )
                char_attempt += 1
                sleep(char_attempt)
                continue
            else:
                logging.warning(
                    f"HTTP error occurred: {ac_err}. Achievement request for {character} failed"
                )
                error_count += 1
                return
        break

    # Current output logic only outputs to the terminal. Need to update this to allow for a file
    print(characteracjson["Character"]["Name"])
