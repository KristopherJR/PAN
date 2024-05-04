import sql

def get_all():
    return sql.execute("SELECT * FROM Summoners")

def get_by_name(summoner_name):
    for summoner in get_all():
        if summoner[3].lower() == summoner_name.lower():
            return summoner
    return None

def get_by_name_and_tag(summoner_name, tag):
    for summoner in get_all():
        if summoner[3].lower() == summoner_name.lower() and summoner[4].lower() == tag.lower():
            return summoner
    return None

def get_by_puuid(puuid):
    for summoner in get_all():
        if summoner[0] == puuid:
            return summoner
    return None