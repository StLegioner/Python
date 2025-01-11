import requests

# Riot Games API key
API_KEY = "YOUR_API_KEY"  # Replace with your API key

def get_summoner_data(summoner_name, region="euw1"):
    """
    Fetch summoner data from Riot Games API.

    :param summoner_name: The name of the summoner (without tags like #777).
    :param region: The region code (e.g., 'euw1', 'na1').
    :return: JSON data with summoner information or None if the request fails.
    """
    # Clean the summoner name
    summoner_name = summoner_name.strip()  # Remove extra spaces
    if "#" in summoner_name:
        summoner_name = summoner_name.split("#")[0]  # Remove the tag if present

    if not summoner_name:
        print("Error: Summoner name cannot be empty.")
        return None

    # Construct the API request
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": API_KEY}

    # Send the API request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching summoner data: {e}")
        return None

if __name__ == "__main__":
    # Replace interactive input with predefined input for environments without stdin
    test_summoner_name = "ExampleSummoner"  # Replace with a default or test summoner name
    region = "euw1"  # Default region
    print(f"Fetching data for summoner: {test_summoner_name} in region {region}...")

    # Request summoner data
    data = get_summoner_data(test_summoner_name, region)
    if data:
        print("Summoner Data:")
        print(data)
    else:
        print("Failed to retrieve summoner data.")
