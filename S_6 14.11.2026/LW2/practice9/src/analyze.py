def analyze(trips,plan,month):
    plan=plan[plan['month']==month]
    fact=trips[trips['month']==month].groupby('route').agg(count=('trip_id','size'),revenue=('cost_rub','sum'))
    pf=plan.merge(fact,on='route',how='left',validate='1:1')
    pf[['count','revenue']]=pf[['count','revenue']].fillna(0).astype(int)
    pf['trips_done_pct']=(pf['count']/pf['plan_trips']*100).round(2)
    pf['revenue_done_pct']=(pf['revenue']/pf['plan_revenue']*100).round(2)
    pf=pf.sort_values('revenue_done_pct',ascending=False)
    return pf
