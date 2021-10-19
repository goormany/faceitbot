import requests
import datetime
import json
from rich.console import Console
from config import *
import os



console = Console()
data_list = []
data_base = []

headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
}

def check_path():
    if os.path.exists(CACHE_PATH):
        pass
    else:
        os.mkdir(CACHE_PATH)
    

def get_data(url=URL, headers=headers):

    r = requests.get(url, headers)
    # with open('r.json', 'w') as f:
    #     json.dump(r.json(), f, indent=4, ensure_ascii=False)

    data = r.json()
    
    win_or_lose = 'None'
    items = data

    for item in items:
        date = item['date']
        matchId = item['matchId']
        map_csgo = item['i1']
        region = item['i0']
        score = item['i18']
        gameMode = item['gameMode']
        sum_rounds = item['i12']
        bestsof = item['bestOf']
        elo = item['elo']

        normal_date = datetime.datetime.fromtimestamp(date/1000)
        normal_date.isoformat()
            
        score = score.split(' / ')
        if score[0] > score[1]:
            win_or_lose = 'Victory'
            score = f'{score[0]} / {score[1]}'
            
        else:
            win_or_lose = 'Defeat'
            score = f'{score[0]} / {score[1]}'
        
        link = f'https://www.faceit.com/ru/csgo/room/{matchId}'


        data_list.append(
            {
                'date': normal_date,
                'map': map_csgo,
                'Match outcome': win_or_lose,
                'region': region,
                'score': score,
                'sum_rounds': sum_rounds,
                'BO': bestsof,
                'new elo': elo,
                'roomID': matchId,
                'gameMode': gameMode,
                'link': link,
            }
        )

    url = f'https://api.faceit.com/stats/v1/stats/matches/{matchId}'
    r = requests.get(url=url, headers=headers)
    data = r.json()
    # items = data[0]['teams'][0]['players'][0]

    # with open('data.json', 'w') as f:
    #     json.dump(items, f, indent=4, ensure_ascii=False)
    items = data[0]

    num_team = 0
    while True:
        if num_team >= 2:
            break
        else:
            for item in items['teams'][num_team]['players']:
                nickname = item['nickname'],

                for player in nickname:
                    if player == 'WonnaCryL':
                        kill = item['i6'],
                        assists = item['i7'],
                        death = item['i8'],
                        kr = item['c3'],
                        kd = item['c2'],
                        hs = item['i13'],
                        hsp = item['c4'],
                        kda = f'{kill[0]}/{death[0]}/{assists[0]}'

                        data_list.append(
                            {
                            'nickname': nickname[0],
                            'kill': kill[0],
                            'assists': assists[0],
                            'death': death[0],
                            'k/r': kr[0],
                            'k/d': kd[0],
                            'k/d/a': kda,
                            'hs count': hs[0],
                            'hs %': hsp[0],
                            }
                        )
                    else:
                        pass
            num_team +=1
        
    if gameMode == '5v5':
        normal_date = str(normal_date)
        with open(f'{CACHE_PATH}/result.json', 'w') as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False, default=str)
    else:
        pass

def redata():

    data_map = data_list[0]
    data_stats = data_list[1]

    date = data_map['date']
    map_csgo = data_map['map']
    outcome = data_map['Match outcome']
    score = data_map['score']
    new_elo = data_map['new elo']
    matchID = data_map['roomID']

    kill = data_stats['kill']
    death = data_stats['death']
    kd = data_stats['k/d']
    hsp = data_stats['hs %']

    link = data_map['link']
    
    data_base.append(
        {
            'Date': date,
            'Map': map_csgo,
            'Outcome': outcome,
            'Score': score,
            'new_elo': new_elo,
            'matchID': matchID,
            'kill': kill,
            'death': death,
            'k/d': kd,
            'hsp': hsp,
            'link': link,
        }
    )
    # os.system(r' > cache/data.json')

    with open(f'{CACHE_PATH}/data.json', 'w') as f:
        json.dump(data_base, f, indent=4, ensure_ascii=False, default=str)

def get_stats():
    check_path()
    get_data()
    redata()

get_stats()

