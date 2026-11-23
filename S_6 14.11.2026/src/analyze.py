# -*- coding: utf-8 -*-
'''Слой 3: расчёт метрик и проверка гипотез. Файлы не читает, графики не рисует.'''
import pandas as pd
from scipy import stats


def overall_kpi(df):
    '''Сводные показатели по всей компании.'''
    return {
        "рейсов": len(df),
        "выручка": int(df["cost_rub"].sum()),
        "средний чек": round(df["cost_rub"].mean()),
        "медианный чек": round(df["cost_rub"].median()),
        "выручка на км": round(df["cost_rub"].sum() / df["distance_km"].sum(), 1),
        "OTD, %": round((~df["is_delayed"]).mean() * 100, 1),
        'доля рейсов дороже 100 тыс. руб., %':round((df['cost_rub']>100000).mean()*100,1),
    }


def kpi_by(df, column):
    '''KPI в разрезе любого признака: перевозчик, месяц, маршрут.'''
    result = (df.groupby(column)
              .agg(trips=("trip_id", "count"),
                   revenue=("cost_rub", "sum"),
                   avg_ticket=("cost_rub", "mean"),
                   otd=("is_delayed", lambda s: (~s).mean() * 100))
              .round(1)
              .sort_values("revenue", ascending=False))
    return result.reset_index()


def compare_otd(df, a, b, alpha=0.05):
    '''Сравнивает доли задержек двух перевозчиков критерием хи-квадрат.'''
    sub = df[df["carrier"].isin([a, b])]
    table = pd.crosstab(sub["carrier"], sub["is_delayed"])
    chi2, p, _, _ = stats.chi2_contingency(table)
    return {"группа A": a, "группа B": b, "chi2": round(chi2, 3),
            "p": round(p, 5), "значимо": bool(p < alpha)}


def worst_and_best_carrier(df, alpha=0.05):
    '''Перевозчики с худшим и лучшим OTD плюс проверка значимости разницы.'''
    otd = df.groupby("carrier")["is_delayed"].mean().sort_values()
    return compare_otd(df, otd.index[-1], otd.index[0], alpha=alpha)


def cargo_delay_test(df,alpha=0.05):
    '''Проверяет связь типа груза и задержек критерием хи-квадрат.'''
    table=pd.crosstab(df['cargo_type'],df['is_delayed'])
    chi2,p,_,_=stats.chi2_contingency(table)
    if p<alpha:
        conclusion='связь типа груза и задержек есть'
    else:
        conclusion='связи типа груза и задержек не обнаружено'
    return {'chi2':round(float(chi2),3),'p':round(float(p),5),'вывод':conclusion}
