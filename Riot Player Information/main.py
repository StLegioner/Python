import requests


# this API_KEY need to be gerated in RIOT dev accaunt every 24 hours. Here's link for generator
# https://developer.riotgames.com/
API_KEY = "RGAPI-fd9aaab8-0bc4-46fa-b5df-3a67ade9aa30"

def get_puuid(game_name, tag_line, region="europe"):

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("puuid")
    except requests.exceptions.HTTPError as error_text:
        print(f"Error gathering PUUID: {error_text}")
        return None

def get_summoner_data_by_puuid(puuid, region="euw1"):

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error gathering summoner data: {e}")
        return None


def get_match_list(puuid, region="europe", count=3):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error gathering match list: {e}")
        return None

def get_match_details(match_id, region="europe"):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error gathering match details: {e}")
        return None

def print_info(match_details, puuid):
    try:
        participants = match_details["info"]["participants"]
        for participant in participants:
            if participant["puuid"] == puuid:
                kills = participant["kills"]
                deaths = participant["deaths"]
                assists = participant["assists"]
                if participant["win"] == True:
                    match_result = "Win"
                else:
                    match_result = "Loose"
                print(f"{participant['riotIdGameName']}'s match info: KDA {kills}/{deaths}/{assists}, {match_result}")
                return
        print(f"Player with PUUID {puuid} not found in this match.")
    except KeyError as e:
        print(f"Error accessing match details: {e}")



if __name__ == "__main__":

    game_name = input("Enter the Riot Name: ")                      #Check name "Larry"
    tag_line  = input("Enter the Riot Tag: ")                       #Check tag "777"
    count = input("Enter count of interested mathches: ")           #Check info https://www.op.gg/summoners/euw/Larry-777
    region = "europe"
    platform_region = "euw1"


    puuid = get_puuid(game_name, tag_line, region)

    if not puuid:
        print("Failed to retrieve PUUID.")
    else:
        #print(f"PUUID retrieved: {puuid}")
        summoner_data = get_summoner_data_by_puuid(puuid, platform_region)
        if not summoner_data:
            print("Failed to retrieve summoner data.")
        else:
            #print(summoner_data)
            print(f"Summoner Name: {game_name}\n"                           
                  f"Summoner level: {summoner_data['summonerLevel']}\n"
                  f"Summoner icon: {summoner_data['profileIconId']}")
    if puuid:

        match_list = get_match_list(puuid, region,count)

        if match_list:
            print(f"Retrieved {len(match_list)} matches:")
            for match_id in match_list:
                #print(f"Match ID: {match_id}")
                match_details = get_match_details(match_id, region)
                if match_details:
                    #print(match_details)
                    print_info(match_details, puuid)
                else:
                    print(f"Failed to retrieve details for match {match_id}.")
        else:
            print("Failed to retrieve match list.")
    else:
        print("Failed to retrieve PUUID.")
# need GUI