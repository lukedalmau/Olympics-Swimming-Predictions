import os
from typing import Dict, List
from tournament import Tournament
import pandas as pd
from concurrent.futures import *

def convert_time(o):
    try:
        o=float(o)
        return float(o)
    except:
        m,s = o.split(':')
        return float(m)*60 + float(s)



def deploy_tournament(config,df, simNum,records_table):

    gender, distance, stroke, poolConfiguration,name_of_file = config

    tournament = Tournament(gender,distance,stroke,poolConfiguration,df)

    podium = tournament.start()

    try:
        records_table[simNum].append({name_of_file:podium})
    except KeyError:
        records_table[simNum] = [{name_of_file: podium}]

def simulationProcess(configs_dfs,i,amount,records_table):
    
    print(f"SIMULATION {i+1}/{amount}...")

    for config, df in configs_dfs:

        deploy_tournament(config,df ,i, records_table) 

        

def fetch_csv(directory):
    configs_dfs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                df = pd.read_csv(file_path, dtype='string')

                name_of_file, _ = file.split(".")

                gender, distance, stroke, poolConfiguration = name_of_file.split("-")  # Configuracion del torneo
                
                config = (gender,distance,stroke,poolConfiguration,name_of_file)

                if stroke.find('RELAY') != -1:
                    df = df[['full_name_computed', 'swim_time',
                            'team_code', 'team_short_name']]

                    df.astype("string")

                    df['swim_time'] = df['swim_time'].apply(convert_time).astype('float64')
                    pass

                else:

                    df = df[['full_name_computed', 'swim_time',
                            'team_code', 'team_short_name']]

                    df.astype("string")

                    df['swim_time'] = df['swim_time'].apply(convert_time).astype('float64')

                    configs_dfs.append((config,df))
    return configs_dfs


def tournament_setup_deploy(amount):

    records_table: Dict[str, List] = {}

    directory = os.path.join("archive-database-sports", "fina-csv-all")

    executor = ThreadPoolExecutor()
    proxecutor = ProcessPoolExecutor()

    config_dfs = fetch_csv(directory)

    print("STARTING SIMULATIONS...")

    tasks = [executor.submit(simulationProcess, config_dfs, i, amount, records_table)for i in range(amount)]

    wait(tasks, return_when=ALL_COMPLETED)

    print("SIMULATIONS DONE...")

    print("REACOMODATING DATA...")


    events = []
    first = []
    first_team_code = []
    first_team=[]
    second = []
    second_team_code = []
    second_team = []
    third = []
    third_team_code = []
    third_team = []

    for simNum,values in records_table.items():
        simNum += 1
        
        for event_podium in values:
            for event,podium in event_podium.items():
                events.append(event)
                first.append(podium[0][0])
                first_team_code.append(podium[0][2])
                first_team.append(podium[0][3])


                second.append(podium[1][0])
                second_team_code.append(podium[1][2])
                second_team.append(podium[1][3])

                third.append(podium[2][0])
                third_team_code.append(podium[2][2])
                third_team.append(podium[2][3])

    data={
        "Events" :events,
        "First Place":first,
        "First Team Code": first_team_code,
        "First Team": first_team,
        "First Place Percentage": [100*(1.0/amount) for _ in range(len(events))],
        "Second Place" : second,
        "Second Team Code": second_team_code,
        "Second Team": second_team,
        "Second Place Percentage": [100*(1.0/amount) for _ in range(len(events))],
        "Third Place" :third,
        "Third Team Code": third_team_code,
        "Third Team": third_team,
        "Third Place Percentage": [100.0*(1.0/amount) for _ in range(len(events))],
    }


    df = pd.DataFrame.from_dict(data)

    df_group_by_first = df[['Events', 'First Place',
                            'First Team Code', 'First Team', 'First Place Percentage']]

    df_group_by_first = df_group_by_first.groupby(
        ['Events', 'First Place', 'First Team Code', 'First Team'], as_index=False).sum().sort_values(
            by=['Events', 'First Place Percentage'], ascending=False)
    
   #print(df_group_by_first.head())
    
    df_group_by_second = df[['Events', 'Second Place',
                             'Second Team Code','Second Team', 'Second Place Percentage']]

    df_group_by_second = df_group_by_second.groupby(
        ['Events', 'Second Place', 'Second Team Code', 'Second Team'], as_index=False).sum().sort_values(
            by=['Events', 'Second Place Percentage'], ascending=False)

    df_group_by_third = df[['Events', 'Third Place',
                            'Third Team Code', 'Third Team', 'Third Place Percentage']]

    df_group_by_third = df_group_by_third.groupby(
        ['Events', 'Third Place', 'Third Team Code', 'Third Team'], as_index=False).sum().sort_values(
            by=['Events', 'Third Place Percentage'], ascending=False)


    df_group_by_first.columns = ['Event','Name','Team Code','Team Name','Percent'] 
    df_group_by_second.columns = ['Event', 'Name','Team Code','Team Name', 'Percent']
    df_group_by_third.columns = ['Event', 'Name','Team Code','Team Name', 'Percent']


    #print(df_group_by_first.head())
   
    first = df_group_by_first.reset_index().drop(['index'], axis=1)

    second = df_group_by_second.reset_index().drop(['index'], axis=1)

    third = df_group_by_third.reset_index().drop(['index'], axis=1)

    #print(df_group_by_first.head())

    first.name = "First Place"
    second.name = "Second Place"
    third.name = "Third Place"

    print("DATA IS READY...\n \n")


    return first,second,third

#print(tournament_setup_deploy(10))
