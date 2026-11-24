import pandas as pd
def load(raw_dir):
    april=pd.read_csv(raw_dir/'trips_april.csv',parse_dates=['date'])
    may=pd.read_csv(raw_dir/'trips_may.csv',parse_dates=['date'])
    plan=pd.read_csv(raw_dir/'plan.csv')
    return april,may,plan
