from pandas.core.frame import DataFrame
import random as r
import math

from typing import Dict,List

class Swimmer:

    def __init__(self,full_name:str,swim_time:float,mean_time:float,variance: float,team_code:str,team_name:str):

        self.full_name:str = full_name
        self.swim_time:float = swim_time
        self.mean_time:float = mean_time
        self.variance:float = variance if not math.isnan(variance)  else 0.00001
        self.team_code:str = team_code
        self.team_name:str = team_name
        
    def Swim(self)->float:
        return  r.normalvariate(self.mean_time,self.variance)
        
        
