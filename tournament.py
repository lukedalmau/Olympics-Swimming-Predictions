from typing import Dict, List,Tuple
from numpy.core.numeric import NaN, True_
from pandas.core.frame import DataFrame
from swimmer import Swimmer
import random


class Tournament:

    def __init__(self,gender:str,distance:str,stroke:str,poolConfiguration:str,df:DataFrame) -> None:
        self.gender = gender
        self.distance = distance
        self.stroke = stroke
        self.poolConfiguration = poolConfiguration
        self.swimmers:List[Swimmer] = self.initializeSwimmers(df)
        self.ranking = {}



    def start(self)->Tuple[Swimmer,Swimmer,Swimmer]:

        eliminatories=[[swimmer,swimmer.swim_time] for swimmer in self.swimmers]

        self.compete(eliminatories)
        
        semifinals = sorted(self.ranking.items(), key=lambda x:x[1])[:16]

        self.ranking.clear()
        for key,value in semifinals:
            self.ranking[key]=value


        self.compete(semifinals)

        semifinal1,semifinal2 = ({},{})

        for i,value in enumerate(self.ranking.items()):
            swimmer,swim_time = value
            if i%2:
                semifinal1[swimmer]=swim_time
            else:
                semifinal2[swimmer]=swim_time
        
        semifinal1 = sorted(semifinal1.items(), key=lambda x:x[1])[:4]
        semifinal2 = sorted(semifinal2.items(), key=lambda x:x[1])[:4]

        semifinal1.extend(semifinal2)

        final = semifinal1

        self.ranking.clear()
        for key,value in semifinals:
            self.ranking[key]=value

        
        self.compete(final)

        final = sorted(self.ranking.items(), key=lambda x:x[1])[:3]

        swimmers = [(swimmer[0].full_name ,i+1 )for i,swimmer in enumerate(final)]

        return swimmers


    def compete(self,swimmers_time: List[Tuple[Swimmer,float]])->None:

        total=len(swimmers_time)
        series_num = int(total/8)
        series=[[]for _ in range(series_num)]
        carriles=[[]for _ in range(8)]
        
        swimmers_time.sort(key=lambda x:x[1],reverse=True)

        swimmers = [x[0] for x in swimmers_time]

        for i,j in zip(range(0,total,series_num),range(8)):
            
            carriles[j].extend(swimmers[i+k]for k in range(series_num))

        for i in range(series_num):
            for j in range(8):
                series[i].append(carriles[j][i])
        
        for serie in series:
            for swimmer in serie:
                self.ranking[swimmer]=swimmer.Swim()


    def initializeSwimmers(self,df: DataFrame)->List[Swimmer]:
        swimmers:List[Swimmer]=[]

        df.fillna(0)
        swim_time_Series = df['swim_time']
        mean_time=swim_time_Series.mean()
        max_time=swim_time_Series.max()
        variance=df['swim_time'].var(ddof=0)

        mean_time=(mean_time+max_time)/2.0

        df.replace(0,random.normalvariate(mean_time,variance))

        df_group_by_swimmers = df.groupby(
            'full_name_computed',as_index=False,sort=False
            )['swim_time'].aggregate(['min','mean','var']
            ).rename(columns={'min':'swim_time','mean':'mean','var':'variance'})
 
        
        for full_name, row in df_group_by_swimmers.iterrows():
            swimmers.append(Swimmer(full_name, row['swim_time'],row['mean'],row['variance']))
        return swimmers
            