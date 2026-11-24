from config import raw_dir,processed_dir,reports_dir,month
from src.load import load
from src.prepare import prepare
from src.analyze import analyze
def main():
    april,may,plan=load(raw_dir)
    trips=prepare(april,may)
    pf=analyze(trips,plan,month)
    processed_dir.mkdir(parents=True,exist_ok=True)
    reports_dir.mkdir(parents=True,exist_ok=True)
    pf.to_csv(processed_dir/'plan_fact.csv',index=False,encoding='utf-8-sig')
    plan_revenue=pf['plan_revenue'].sum()
    revenue=pf['revenue'].sum()
    done=(pf['revenue']>=pf['plan_revenue']).sum()
    routes=pf.loc[(pf['count']>pf['plan_trips']) & (pf['revenue']<pf['plan_revenue']),'route']
    report=[
        f'План/факт по маршрутам за {month}',
        f'Суммарный план: {plan_revenue} руб.',
        f'Фактически: {revenue} руб.',
        f'План выполнен на: {revenue/plan_revenue*100:.2f}%' if plan_revenue else 'План по выручке отсутствует',
        f'Выполнили план по выручке: {done}',
        f'Не выполнили: {len(pf)-done}',
        'Рейсов больше плана при выручке ниже плана: '+('; '.join(routes) or 'нет'),
        '',
        pf.to_string(index=False)
    ]
    text='\n'.join(report)
    (reports_dir/'report.txt').write_text(text,encoding='utf-8')
    print(text)
if __name__=='__main__':
    main()
