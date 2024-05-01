import os
import requests

def handle_user_messages(msg) -> str:
    if validate_message(msg) == False:
        return ""

    message_parts = msg.split()
    command = message_parts[0]

    match command:
        case "/grog":
            return "Mmm... need some."
        case "/game":
            if len(message_parts) > 1:
                summoner_name = msg.replace("/game ", "")
                return get_live_game(summoner_name)
            else:
                return "Give me a summoner name, bub."
        case _:
            return ""

def validate_message(msg) -> bool:
    if msg.count('/') != 1:
        return False

def get_riot_api_token() -> str:
    return os.getenv("RIOT_API_TOKEN")

def get_live_game(summoner_name) -> str:
    puuid = get_puuid(summoner_name)
    token = get_riot_api_token()
    response = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}", headers={"X-Riot-Token": token})

    if (response.status_code == 404):
        return f"{summoner_name} is not currently in a game. What are you stupid?"
    if (response.status_code == 200):
        return response.content

def get_puuid(summoner_name) -> str:
    match summoner_name.lower():
        case "trinityburst":
            return "NawRoKFxfqWRCNvFRXSMDYGVaJQYsiLRpaNeIisdeMyy-3tJqS-YntU-zv15XVeoehmUVTEdtJfPCQ"
        case "somnus":
            return "3SkR0ZxsiB4mSK1sNt7lyHIdd_5gU0lVLxC3aJzsD9Ics7v7ijCGYU8v-yWwE289vZAM_gIE14y0wA"
        case "wheels":
            return "J_ZQ5LcyQ2bKPc0sdX0O7hZXLZBqiXO2pbrdjV6xAHW76oFBsHwAXSIwNqvSWf5--J2VS7aaTY7U7Q"
        case "smol keigo":
            return "J-PuAH8-ty3o1d_PrkDe4Ip8bY2lQmpndBr8dmAnLYdcg0C4wUtTCUMtKsixgUfsqn5PpBgdWrsebA"

# def get_summoner_name(puuid) -> str:
#     match summoner_name.lower():
#         case "NawRoKFxfqWRCNvFRXSMDYGVaJQYsiLRpaNeIisdeMyy-3tJqS-YntU-zv15XVeoehmUVTEdtJfPCQ":
#             return 
#         case "somnus":
#             return "3SkR0ZxsiB4mSK1sNt7lyHIdd_5gU0lVLxC3aJzsD9Ics7v7ijCGYU8v-yWwE289vZAM_gIE14y0wA"
#         case "wheels":
#             return "J_ZQ5LcyQ2bKPc0sdX0O7hZXLZBqiXO2pbrdjV6xAHW76oFBsHwAXSIwNqvSWf5--J2VS7aaTY7U7Q"
#         case "smol keigo":
#             return "J-PuAH8-ty3o1d_PrkDe4Ip8bY2lQmpndBr8dmAnLYdcg0C4wUtTCUMtKsixgUfsqn5PpBgdWrsebA"