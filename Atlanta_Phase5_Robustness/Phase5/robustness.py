import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf, matplotlib.pyplot as plt
from pathlib import Path
from zipfile import ZipFile
from scipy.stats import t
D=Path('/mnt/data'); O=D/'Phase5'
p=pd.read_csv(D/'Phase4_results/panel.csv',dtype={'ZCTA':str}); x=p.drop_duplicates(['ZCTA','Destination']).drop(columns=['Month','flow']); w=pd.read_csv(D/'Phase4_results/crosswalk.csv',dtype={'GEOID':str,'ZCTA':str}); v=pd.read_csv(ZipFile(D/'Atlanta_Foot_Traffic_2024.zip').open('Origin_Destination_Flows.csv'),dtype={'Origin_CBG':str}); rows=[]
def fit(d,label,kind='PPML'):
 d=d.dropna(subset=['log_income','log_pop','log_distance']).copy(); d['income_luxury']=d.log_income*d.luxury
 for model,rhs in [('Gravity','log_distance + log_income + log_pop + C(Destination) + C(Month)'),('Sorting','log_distance + income_luxury + C(ZCTA) + C(Destination) + C(Month)')]:
  if kind=='OLS': d=d[d.flow>0].copy(); d['log_flow']=np.log(d.flow); m=smf.ols('log_flow ~ '+rhs,d).fit(cov_type='cluster',cov_kwds={'groups':d.ZCTA})
  else: m=smf.glm('flow ~ '+rhs,d,family=sm.families.Poisson()).fit(cov_type='cluster',cov_kwds={'groups':d.ZCTA})
  G=d.ZCTA.nunique(); crit=t.ppf(.975,G-1)
  for term in ['log_distance','log_income','income_luxury']:
   if term in m.params:
    b,s=m.params[term],m.bse[term]; rows.append([label,kind,model,term,b,s,2*t.sf(abs(b/s),G-1),b-crit*s,b+crit*s,len(d),G])
def panel(weights,period):
 a=v[v.Period==period].merge(weights,left_on='Origin_CBG',right_on='GEOID'); a['flow']=a.Device_Count*a.weight; q=a.groupby(['ZCTA','Mall','Month']).flow.sum().reset_index().rename(columns={'Mall':'Destination'}); return x.merge(q,on=['ZCTA','Destination'])
fit(p,'Area baseline'); fit(p,'Log-linear','OLS'); fit(panel(w,'Weekday'),'Weekday'); fit(panel(w,'Weekend'),'Weekend'); fit(p[p.Month<=10],'Jan-Oct'); fit(p[p.Month>=11],'Nov-Dec'); fit(panel(w[w.weight>=.999],'All'),'Contained CBGs'); mx=w.sort_values('weight').drop_duplicates('GEOID',keep='last'); mx=mx[mx.weight>.5].copy(); mx.weight=1; fit(panel(mx,'All'),'Majority area');
for z in sorted(p.dropna(subset=['income']).ZCTA.unique()): fit(p[p.ZCTA!=z],'Omit '+z)
r=pd.DataFrame(rows,columns=['sample','estimator','model','term','coef','se','p_t','lower','upper','n','clusters']); r.to_csv(O/'robustness.csv',index=False); print(r[~r['sample'].str.startswith('Omit')].to_string(index=False)); print(r[r['sample'].str.startswith('Omit')].groupby(['model','term']).agg(min_coef=('coef','min'),max_coef=('coef','max'),max_p=('p_t','max')))
for model,term in [('Gravity','log_distance'),('Sorting','income_luxury')]:
 a=r[(r.model==model)&(r.term==term)&~r['sample'].str.startswith('Omit')]; fig,ax=plt.subplots(figsize=(8,5)); ax.errorbar(a.coef,range(len(a)),xerr=[a.coef-a.lower,a.upper-a.coef],fmt='o'); ax.set_yticks(range(len(a)),a['sample']); ax.axvline(0,ls='--'); ax.set_title(model+' : '+term+' (cluster t intervals)'); fig.tight_layout(); fig.savefig(O/(model+'.png')); plt.close(fig)
