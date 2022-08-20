from helpers.request import xivapi_request


def get_fc_info(fc_id, privatekey):
    fc_request = (
        f"https://xivapi.com/freecompany/{fc_id}?columns=FreeCompany.ActiveMemberCount,"
        f"FreeCompany.ID,FreeCompany.Name,FreeCompany.Server,FreeCompany.Tag"
    )

    # Adding in the user's API key if provided
    if privatekey:
        fc_request += f"&private_key={privatekey}"

    # Retrieving general FC information
    fc_data = xivapi_request(fc_request)

    if fc_data:
        print(f"Successfully pulled basic FC data")
        return fc_data
    else:
        print(f"Failed to pull basic FC data. Exiting.")
        exit()


def get_fc_members(fc_id, privatekey):
    # Retrieving FC members list

    fc_member_request = (
        f"https://xivapi.com/freecompany/{fc_id}?data=FCM&columns=FreeCompanyMembers.*.ID,"
        f"FreeCompanyMembers.*.Name"
    )

    # Adding in the user's API key if provided
    if privatekey:
        fc_member_request += f"&private_key={privatekey}"

    fc_member_list = xivapi_request(fc_member_request)

    if fc_member_list:
        print(f"Successfully pulled FC member list")
        return fc_member_list
    else:
        print(f"Failed to pull FC member list. Exiting.")
        exit()


def character_output(privatekey, character):

    character_request = (
        f"https://xivapi.com/character/{character}?columns=Character.Name"
    )

    # Adding in the user's API key if provided
    if privatekey:
        character_request += f"&private_key={privatekey}"

    character_json = xivapi_request(character_request)

    # Current output logic only outputs to the terminal. Need to update this to allow for a file
    print(character_json["Character"]["Name"])

    return


def get_fc_census(character):
    pass
