from pandas.core.frame import DataFrame
import random as r
import math

from typing import Any,List

class Swimmer:

    def __init__(self,full_name:str,swim_time:float,mean_time:float,variance: float,team_code:str,team_name:str):

        self.full_name:str = full_name
        self.swim_time:float = swim_time
        self.mean_time:float = mean_time
        self.variance:float = variance if not math.isnan(variance)  else 0.00001
        self.team_code:str = team_code
        self.team_name:str = team_name
    
    def __str__(self) -> str:
        return f'Name:{self.full_name} BT:{self.swim_time} MT:{self.mean_time} \n Var:{self.variance} Code:{self.team_code} Team:{self.team_name}'
    def __repr__(self) -> str:
        return self.__str__()

    def Swim(self,swimmers:List[Any] = None)->float:

        if not swimmers is None:

            sum_var_swimmers = sum([s.variance for s in swimmers])

            mean_var_swimmers = sum_var_swimmers/len(swimmers)

            self_conditioned_var = (self.variance + mean_var_swimmers)/2.0
        else:
            self_conditioned_var = self.variance

        return  r.normalvariate(self.mean_time,self_conditioned_var)
        
        
