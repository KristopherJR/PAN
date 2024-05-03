import requests
import os
import sqlite3
from dotenv import load_dotenv

def get_live_game(summoner_name) -> str:    
    puuid = get_puuid(summoner_name)
    token = get_riot_api_token()
    response = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}", headers={"X-Riot-Token": token})
    if (response.status_code == 404):
        return f"{summoner_name} is not currently in a game. What are you stupid?"
    if (response.status_code == 200):
        return response.content
    return f"{response.status_code}: An error occured communicating with the Riot API."

def get_puuid(summoner_name) -> str:
    #lookup the name in the db
    connection = sqlite3.connect("league.db")
    cursor = connection.cursor()
    cursor.execute("SELECT PUUID FROM Summoners WHERE ")
    #if cant find it, get the puuid from riot api

def get_riot_api_token() -> str:
    load_dotenv()
    return os.getenv("RIOT_API_TOKEN")

def register(summoner_name, tag) -> str:
    #if tag contains a hash, remove it
    if tag.count('#') > 0:
        tag = tag.replace('#', '')
    
    #lookup the name in the db
    connection = sqlite3.connect("league.db")
    cursor = connection.cursor()
    result = cursor.execute(f"SELECT PUUID FROM Summoners WHERE Summoner_Name='{summoner_name}' AND Tag='{tag}'")
    if result.fetchone() is None:
        token = get_riot_api_token()
        response = requests.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}?api_key={token}")
        if (response.status_code == 404):
            return f"{summoner_name} #{tag} could not be found on EUW."
        if (response.status_code == 200):
            detail = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{response.json()["puuid"]}?api_key={get_riot_api_token()}").json()
            sql = "INSERT INTO Summoners (PUUID, Encrypted_Summoner_ID, Encrypted_Account_ID, Summoner_Name, Tag) VALUES (?, ?, ?, ?, ?)"
            data = (detail["puuid"], detail["id"], detail["accountId"], summoner_name, tag)
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
            return f"Successfully registered {summoner_name} #{tag}!"
        return f"{response.status_code}: An error occurred communicating with the Riot API."
    else:
        return f"{summoner_name} #{tag} is already registered!"