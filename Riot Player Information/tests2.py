import requests

# Riot Games API key
API_KEY = "RGAPI-ef188ab8-7ce7-4c4f-9051-417b78a52326"  # Replace with your actual API key

def get_puuid(game_name, tag_line, region="europe"):
    """
    Fetch the PUUID for a given Riot ID (gameName and tagLine).

    :param game_name: The game name part of the Riot ID.
    :param tag_line: The tag line part of the Riot ID.
    :param region: The regional routing value (e.g., 'europe', 'americas', 'asia').
    :return: PUUID as a string or None if the request fails.
    """
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("puuid")
    except requests.exceptions.HTTPError as error_text:
        print(f"Error fetching PUUID: {error_text}")
        return None

def get_summoner_data_by_puuid(puuid, region="euw1"):
    """
    Fetch summoner data using the PUUID.

    :param puuid: The player's universally unique identifier.
    :param region: The platform routing value (e.g., 'euw1', 'na1').
    :return: JSON data with summoner information or None if the request fails.
    """
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching summoner data: {e}")
        return None

if __name__ == "__main__":
    # Prompt user for Riot ID
    riot_id = input("Enter the Riot ID (format: gameName#tagLine): ")
    if "#" not in riot_id:
        print("Invalid Riot ID format. Please use 'gameName#tagLine'.")
    else:
        game_name, tag_line = riot_id.split("#")
        region = "europe"  # Regional routing value for Account-V1 API
        platform_region = "euw1"  # Platform routing value for Summoner-V4 API

        print(f"Fetching PUUID for Riot ID: {game_name}#{tag_line} in region {region}...")
        puuid = get_puuid(game_name, tag_line, region)

        if puuid:
            print(f"PUUID retrieved: {puuid}")
            print(f"Fetching summoner data for PUUID in region {platform_region}...")
            summoner_data = get_summoner_data_by_puuid(puuid, platform_region)
            if summoner_data:
                print("Summoner Data:")
                print(summoner_data)
            else:
                print("Failed to retrieve summoner data.")
        else:
            print("Failed to retrieve PUUID.")