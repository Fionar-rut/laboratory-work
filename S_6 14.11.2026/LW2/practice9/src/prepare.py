import pandas as pd
def prepare(april,may):
    trips=pd.concat([april,may],ignore_index=True)
    trips['month']=trips['date'].dt.to_period('M').astype(str)
    return trips
