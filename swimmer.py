from pandas.core.frame import DataFrame
import random as r
import math

from typing import Dict,List

class Swimmer:

    def __init__(self,full_name:str,swim_time:float,mean_time:float,variance: float):

        self.full_name:str = full_name
        self.swim_time:float = swim_time
        self.mean_time:float = mean_time
        self.variance:float = variance if not math.isnan(variance)  else 0.00001

        
    def Swim(self)->float:
        return  r.normalvariate(self.mean_time,self.variance)
        
        
