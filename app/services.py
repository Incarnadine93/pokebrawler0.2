import requests , json


def roundDrivers(round):
    d_list = []
    x = r.get(f"http://ergast.com/api/f1/2010/{round}/drivers.json")
    d = x.json()
    y = d['MRData']['DriverTable']['Drivers']
    for a in y:
        d_list.append(a['driverId'])
    return d_list



def getDriver(st):
    x = r.get(f'http://ergast.com/api/f1/drivers/{st}.json')
    d = x.json()
    # print(d)
    driver = {}
    first_name = d['MRData']['DriverTable']['Drivers'][0]['givenName']
    last_name = d['MRData']['DriverTable']['Drivers'][0]['familyName']
    nation = d['MRData']['DriverTable']['Drivers'][0]['nationality']
    driver['id'] = st
    driver['first_name'] = first_name
    driver['last_name'] = last_name
    driver['nation'] = nation
    return driver

def findpokemon(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        my_dict = response.json()
        pokemon_dict = {}
        pokemon_dict["Name"] = my_dict["name"]
        pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
        pokemon_dict["Front_Shiny"] = my_dict["sprites"]["other"]["official-artwork"]["front_default"]
        pokemon_dict["Base_ATK"] = my_dict["stats"][1]["base_stat"]
        pokemon_dict["Base_HP"] = my_dict["stats"][0]["base_stat"]
        pokemon_dict["Base_DEF"] = my_dict["stats"][2]["base_stat"]
        return pokemon_dict

