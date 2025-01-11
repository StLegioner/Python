import requests

API_KEY = "RGAPI-ef188ab8-7ce7-4c4f-9051-417b78a52326"

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

if __name__ == "__main__":

    game_name = input("Enter the Riot Name: ")
    tag_line  = input("Enter the Riot Tag: ")
    region = "europe"
    platform_region = "euw1"

    print(f"Gathering PUUID for Riot ID: {game_name}#{tag_line} in region {region}...")
    puuid = get_puuid(game_name, tag_line, region)

    if not puuid:
        print("Failed to retrieve PUUID.")
    else:
        print(f"PUUID retrieved: {puuid}")
        print(f"Gathering summoner data for PUUID in region {platform_region}...")
        summoner_data = get_summoner_data_by_puuid(puuid, platform_region)
        if not summoner_data:
            print("Failed to retrieve summoner data.")
        else:
            print(summoner_data)
            print(f"Summoner Name: {game_name}\n"
                  f"Summoner level: {summoner_data['summonerLevel']}\n"
                  f"Summoner icon: {summoner_data['profileIconId']}")
# need GUI