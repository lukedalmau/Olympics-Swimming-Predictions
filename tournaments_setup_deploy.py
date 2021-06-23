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



def deploy_tournament(file,root, simNum,records_table):

    file_path = os.path.join(root,file)

    df = pd.read_csv(file_path,dtype= 'string')

    name_of_file , _ = file.split(".")

    gender, distance, stroke, poolConfiguration = name_of_file.split("-") #Configuracion del torneo

    if stroke.find('RELAY')!=-1:
        df = df[['full_name_computed', 'swim_time',
                 'team_code', 'team_short_name']]
    
        df.astype("string")

        df['swim_time']=df['swim_time'].apply(convert_time).astype('float64')
        pass

    else:

        df = df[['full_name_computed','swim_time','team_code','team_short_name']]
        
        df.astype("string")

        df['swim_time']=df['swim_time'].apply(convert_time).astype('float64')

        tournament = Tournament(gender,distance,stroke,poolConfiguration,df)

        podium = tournament.start()

        try:
            records_table[simNum].append({name_of_file:podium})
        except KeyError:
            records_table[simNum] = [{name_of_file: podium}]

def simulationProcess(directory,i,records_table):
    for root,dirs,files in os.walk(directory):

        executor = ThreadPoolExecutor()

        tasks = [ executor.submit(deploy_tournament, file, root, i, records_table) 
        if file.endswith(".csv")
        else executor.submit(print, "No CSV file")
        for file in files]
        wait(tasks,return_when=ALL_COMPLETED)


def tournament_setup_deploy(amount):

    records_table: Dict[str, List] = {}

    directory = os.path.join("archive-database-sports", "fina-csv-all")

    executor = ThreadPoolExecutor()
    
    for i in range(amount):
        simulationProcess(directory , i,records_table )

    events = []
    first = []
    first_team = []
    second = []
    second_team = []
    third = []
    third_team = []

    for simNum,values in records_table.items():
        simNum += 1
        
        for event_podium in values:
            for event,podium in event_podium.items():
                events.append(event)
                first.append(podium[0][0])
                first_team.append(podium[0][2])

                second.append(podium[1][0])
                second_team.append(podium[1][2])

                third.append(podium[2][0])
                third_team.append(podium[2][2])
    data={
        "Events" :events,
        "First Place":first,
        "First Team": first_team,
        "First Place Percentage": [100*(1.0/amount) for _ in range(len(events))],
        "Second Place" : second,
        "Second Team": second_team,
        "Second Place Percentage": [100*(1.0/amount) for _ in range(len(events))],
        "Third Place" :third,
        "Third Team": third_team,
        "Third Place Percentage": [100.0*(1.0/amount) for _ in range(len(events))],
    }


    df = pd.DataFrame.from_dict(data)

    df_group_by_first = df[['Events','First Place','First Team','First Place Percentage']]

    df_group_by_first = df_group_by_first.groupby(
        ['Events', 'First Place','First Team'], as_index=False).sum().sort_values(by=['Events', 'First Place Percentage'], ascending=False)
    
   #print(df_group_by_first.head())
    

    df_group_by_second = df[['Events', 'Second Place','Second Team', 'Second Place Percentage']]

    df_group_by_second = df_group_by_second.groupby(
        ['Events', 'Second Place','Second Team'], as_index=False).sum().sort_values(by=['Events', 'Second Place Percentage'], ascending=False)


    df_group_by_third = df[['Events', 'Third Place','Third Team', 'Third Place Percentage']]

    df_group_by_third = df_group_by_third.groupby(
        ['Events', 'Third Place','Third Team'], as_index=False).sum().sort_values(by=['Events', 'Third Place Percentage'], ascending=False)


    df_group_by_first.columns = ['Event','Name','Team','Percent'] 
    df_group_by_second.columns = ['Event', 'Name','Team', 'Percent']
    df_group_by_third.columns = ['Event', 'Name','Team', 'Percent']


    #print(df_group_by_first.head())
   
    first = df_group_by_first.reset_index().drop(['index'], axis=1)

    second = df_group_by_second.reset_index().drop(['index'], axis=1)

    third = df_group_by_third.reset_index().drop(['index'], axis=1)

    #print(df_group_by_first.head())

    first.name = "First Place"
    second.name = "Second Place"
    third.name = "Third Place"



    return first,second,third

#print(tournament_setup_deploy(10))
