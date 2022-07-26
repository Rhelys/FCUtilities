import requests
from requests.exceptions import HTTPError
import logging
from multiprocessing.pool import Pool
from time import time, sleep

startTime = time()

privatekeyfile = open("private.txt", "r")
privatekey = privatekeyfile.read()


def characteroutput(character):
    if privatekey != '':
        requesturl = f'https://xivapi.com/character/{character}?columns=Character.Name' \
                     f'&private_key={privatekey}'
    else:
        requesturl = f'https://xivapi.com/character/{character}?columns=Character.Name'

    char_attempt = 1
    error_count = 0

    while True:
        try:
            response = requests.get(requesturl)
            response.raise_for_status()
            characteracjson = response.json()
        except HTTPError as char_http_err:
            if char_attempt <= 3:
                logging.info(f'HTTP error occurred: {char_http_err}. Trying {4 - char_attempt} more time(s)')
                char_attempt += 1
                sleep(char_attempt)
                continue
            else:
                logging.warning(f'HTTP error occurred: {char_http_err}. Achievement request for {character} failed')
                error_count += 1
                return
        except Exception as ac_err:
            if char_attempt <= 3:
                logging.info(f'HTTP error occurred: {ac_err}. Trying {4 - char_attempt} more time(s)')
                char_attempt += 1
                sleep(char_attempt)
                continue
            else:
                logging.warning(f'HTTP error occurred: {ac_err}. Achievement request for {character} failed')
                error_count += 1
                return
        break

    print(characteracjson['Character']['Name'])


if __name__ == '__main__':

    freeCompanyID = input("Enter FC ID: ")
    fcDataRequestUrl = f"https://xivapi.com/freecompany/{freeCompanyID}?columns=FreeCompany.ActiveMemberCount," \
                       f"FreeCompany.ID,FreeCompany.Name,FreeCompany.Server,FreeCompany.Tag"
    fcMembersRequestUrl = f"https://xivapi.com/freecompany/{freeCompanyID}?data=FCM&columns=FreeCompanyMembers.*.ID," \
                          f"FreeCompanyMembers.*.Name"

    # Retrieving general FC information
    attempt = 1
    while True:
        try:
            fcDataApiResponse = requests.get(fcDataRequestUrl)
            fcDataApiResponse.raise_for_status()
            fcDataJson = fcDataApiResponse.json()
        except HTTPError as http_err:
            if attempt <= 3:
                logging.warning(f'HTTP error occurred during FC data request: {http_err}. Retrying {4 - attempt} more '
                                f'time(s)')
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.critical(f'Final HTTP error occurred during FC data request: {http_err}. Failed to get info '
                                 f'for FC ID: {freeCompanyID}')
        except Exception as err:
            if attempt <= 3:
                logging.warning(f'Other error occurred: {err}. Retrying {4 - attempt} more time(s)')
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(f'Other error occurred: {err}. Failed to get info for FC ID: {freeCompanyID}')
        break

    # Retrieving FC members list
    attempt = 1
    while True:
        try:
            fcMembersApiResponse = requests.get(fcMembersRequestUrl)
            fcMembersApiResponse.raise_for_status()
            fcMembersJson = fcMembersApiResponse.json()
        except HTTPError as http_err:
            if attempt <= 3:
                logging.warning(f'HTTP error occurred: {http_err}. Retrying {4 - attempt} more time(s)')
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(f'HTTP error occurred: {http_err}. Failed to get members for FC ID: {freeCompanyID}')
        except Exception as err:
            if attempt <= 3:
                logging.warning(f'Other error occurred: {err}. Retrying {4 - attempt} more time(s)')
                attempt += 1
                sleep(attempt)
                continue
            else:
                logging.error(f'Other error occurred: {err}. Failed to get members for FC ID: {freeCompanyID}')
        break

    # Setting FC member count for later
    fcMemberCount = fcDataJson["FreeCompany"]["ActiveMemberCount"]
    fcName = fcDataJson["FreeCompany"]["Name"]
    fcMemberIds = [f['ID'] for f in fcMembersJson["FreeCompanyMembers"]]

    print(f'\n{fcName} has {fcMemberCount} members\n')

    with Pool(4) as p:
        # Return format [ucob_count, uwu_count, tea_count, hidden_achievements, error_count]
        thread_finals = p.map(characteroutput, fcMemberIds)

    finalTime = time() - startTime
    print(f'Script took {"{:.2f}".format(finalTime)} seconds')

# print(fcMembersJson["FreeCompanyMembers"][0]["ID"])
# Black Waltz ID: 9229001536389057973
# Kings FC ID: 9229001536388989429
# Bungo FC ID (Mill): 9232238498621260475
