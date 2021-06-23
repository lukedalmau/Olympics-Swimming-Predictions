import os
import requests
from concurrent.futures import *
import time

# genders=['M','F','X']

# distances=['50','100','200','400','800','1500']

# strokes=['FREESTYLE','BACKSTROKE','BREASTSTROKE','BUTTERFLY','MEDLEY','FREESTYLE_RELAY','MEDLEY_RELAY']

poolConfigurations=['LCM']

executor = ProcessPoolExecutor()


events={
    'FREESTYLE':{
        'genders':['M','F'],
        'distances':['50','100','200','400','800','1500']
    },
    'BACKSTROKE':{
        'genders':['M','F'],
        'distances':['100','200']
    },
    'BREASTSTROKE':{
        'genders':['M','F'],
        'distances':['100','200']
    },
    'BUTTERFLY':{
        'genders':['M','F'],
        'distances':['100','200']
    },
    'MEDLEY':{
        'genders':['M','F'],
        'distances':['200','400']
    },
    'FREESTYLE_RELAY':{
        'genders':['M','F'],
        'distances':['50','100','200','400','800','1500']
    },
    'MEDLEY_RELAY':{
        'genders':['M','F','X'],
        'distances':['100']
    }
}

def csv_downloader(gender,distance,stroke,poolConfiguration):
    attempts = 3

    for _ in range(attempts):
        
        head = 'https://api.fina.org/fina/rankings/swimming/report/csv?'

        tail = '&year=&startDate=&endDate=&timesMode=ALL_TIMES&regionId=&countryId=&pageSize=200'

        name = gender+"-"+distance+"-"+stroke+"-"+poolConfiguration+'.csv'
                    
        mid = 'gender='+gender+'&distance='+distance+'&stroke='+stroke+'&poolConfiguration='+poolConfiguration+''
        
        url = head+mid+tail

        address = r'./archive-database-sports/fina-csv-all/'+ name

        if os.path.exists(address):
            print(f'Already downloaded... skipping {name}')    
            break
        
        print(f'Downloading {name}')
        
        myfile = requests.get(url, allow_redirects=True)
        
        print(myfile.status_code,f"at {name}")

        if myfile.status_code==200:
            print(f"OK at {name}")
            open(address, 'wb').write(myfile.content)
            break
        else:
            print(f"ERROR in {name}")
    else:
        print(f"Max number of attempts reached at {name}")

for stroke, dictio in events.items():
    genders , distances = dictio.values()
    for gender in genders:
        for distance in distances:
            for poolConfiguration in poolConfigurations:

                executor.submit(csv_downloader,gender,distance,stroke,poolConfiguration)

                

