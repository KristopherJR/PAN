import requests
import os
import sql
import summoner
import sqlite3
from dotenv import load_dotenv

def get_live_game(summoner_name) -> str:
    summ = summoner.get_by_name(summoner_name)

    if summ is None:
        return "I ain't heard of that summoner before!\n\nRegister um with: `/register summoner_name tag`"

    response = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{summ[0]}", headers={"X-Riot-Token": get_riot_api_token()})
    if (response.status_code == 404):
        return f"{summoner_name} is not currently in a game. What are you stupid?"
    if (response.status_code == 200):
        return response.content[:500]
    return f"{response.status_code}: An error occured communicating with the Riot API."

def get_riot_api_token() -> str:
    load_dotenv()
    return os.getenv("RIOT_API_TOKEN")

def register(summoner_name, tag) -> str:
    return_message = ""
    #if tag contains a hash, remove it
    if tag.count('#') > 0:
        tag = tag.replace('#', '')
    
    summ = summoner.get_by_name_and_tag(summoner_name, tag)

    if summ:
        return_message = f"{summ[3]} #{summ[4]} is already registered!"
    else:
        token = get_riot_api_token()
        api_response = requests.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}?api_key={token}")
        if (api_response.status_code == 404):
            return_message = f"{summoner_name} #{tag} could not be found on EUW."
        elif (api_response.status_code == 200):
            detail = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{api_response.json()["puuid"]}?api_key={token}").json()
            data = (detail["puuid"], detail["id"], detail["accountId"], summoner_name, tag)
            try:
                sql.execute("INSERT INTO Summoners (PUUID, Encrypted_Summoner_ID, Encrypted_Account_ID, Summoner_Name, Tag) VALUES (?, ?, ?, ?, ?)", data)
                return_message = f"Successfully registered {summoner_name} #{tag}!"
            except sqlite3.Error as e:
                return_message = "Something went very wrong. Should probs tell @Paninoki."
        else:
            return_message = f"{api_response.status_code}: An error occurred communicating with the Riot API."
    return return_message

