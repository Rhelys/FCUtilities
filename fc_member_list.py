import logging
from multiprocessing.pool import Pool
from time import time
from functools import partial

from helpers import xivapi

import os.path

startTime = time()

if __name__ == "__main__":
    # Setting up the user's API Key if it exists
    privatekey = False

    if os.path.exists("private.txt"):
        privatekeyfile = open("private.txt", "r")
        privatekey = privatekeyfile.read()

    # Taking the FC ID as input for the rest of the calls
    fc_id = input("Enter FC ID: ")

    # Pulling in starting data for the FC
    fc_basic_info = xivapi.get_fc_info(fc_id, privatekey)
    fc_member_info = xivapi.get_fc_members(fc_id, privatekey)

    # Setting FC member count for later
    fc_member_count = fc_basic_info["FreeCompany"]["ActiveMemberCount"]
    fc_name = fc_basic_info["FreeCompany"]["Name"]
    fc_member_ids = [f["ID"] for f in fc_member_info["FreeCompanyMembers"]]

    print(f"\n{fc_name} has {fc_member_count} members\n")

    with Pool(4) as p:
        # Threading calls out to get the list of characters
        thread_finals = p.map(partial(xivapi.character_output, privatekey), fc_member_ids)

    finalTime = time() - startTime
    print(f'Script took {"{:.2f}".format(finalTime)} seconds')

# print(fcMembersJson["FreeCompanyMembers"][0]["ID"])
# Large FC - Black Waltz ID: 9229001536389057973
# Medium FC - Kings FC ID: 9229001536388989429
# Small FC - Bungo FC ID (Mill): 9232238498621260475

# Character ID - Rhelys Infinis: 10488014
