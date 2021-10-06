#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jeb@GEUS.dk

run each 'cell' with CNTL Enter

"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit
from scipy import stats
global out_concept

fs=18
th=1
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
# plt.rcParams['axes.grid'] = False
# plt.rcParams['grid.alpha'] = 0
plt.rcParams['grid.alpha'] = 1
co=0.9; plt.rcParams['grid.color'] = (co,co,co)
plt.rcParams["font.size"] = fs
plt.rcParams['legend.fontsize'] = fs*0.8
plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams["legend.framealpha"]=1

i_year=1992 ; f_year=2020 ; n_years=f_year-i_year+1
years=np.arange(n_years)+i_year

#%% monthly NAO
# available from https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
fn='/Users/jason/Dropbox/NAO/CPC/norm.nao.monthly.b5001.current.ascii'
df_nao=pd.read_csv(fn,delim_whitespace=(True),names=['year','month','NAO'])
df_nao['mon']=''
for i in range(len(df_nao)):df_nao['mon'][i]=str(df_nao['month'][i]).zfill(2)
df_nao['date'] = pd.to_datetime(df_nao['year'].astype(str)+df_nao['mon'].astype(str), format='%Y%m')

df_nao['year'] = pd.DatetimeIndex(df_nao['date']).year
df_nao['month'] = pd.DatetimeIndex(df_nao['date']).month

NAO_monthly=np.zeros((12,n_years))
NAO_JJA=np.zeros(n_years)
NAO_JJAS=np.zeros(n_years)
NAO_ANN=np.zeros(n_years)

for yy in range(n_years):
    for mm in range(12):
        NAO_monthly[mm,yy]=np.mean(df_nao.NAO[((df_nao.year==yy+i_year)&(df_nao.month==mm+1))])
    NAO_JJA[yy]=np.mean(NAO_monthly[5:7,yy])
    NAO_JJAS[yy]=np.mean(NAO_monthly[5:8,yy])
    NAO_ANN[yy]=np.mean(NAO_monthly[:,yy])

plt.plot(years,NAO_JJA,label='JJA')
plt.plot(years,NAO_JJAS,label='JJAS')
plt.plot(years,NAO_ANN,label='ANN')
plt.title('NAO')
plt.title('NAO')
plt.legend()


#%% monthly Greenland Mass Blance
# available from https://dataverse01.geus.dk/dataset.xhtml?persistentId=doi:10.22008/FK2/OHI23Z

fn='/Users/jason/Dropbox/TMB_Mankoff/dataverse_files/MB_SMB_D_BMB.csv' 
df=pd.read_csv(fn)

df['date'] = pd.to_datetime(df['time'])

df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['day'] = pd.DatetimeIndex(df['date']).day

GrMB=np.zeros((12,n_years))
GrMB_JJA=np.zeros(n_years)
GrMB_JJAS=np.zeros(n_years)
GrMB_ANN=np.zeros(n_years)

for yy in range(n_years):
    for mm in range(12):
        GrMB[mm,yy]=np.sum(df.MB[((df.year==yy+i_year)&(df.month==mm+1))])
    GrMB_JJA[yy]=np.sum(GrMB[5:7,yy])
    GrMB_JJAS[yy]=np.sum(GrMB[5:8,yy])
    GrMB_ANN[yy]=np.sum(GrMB[:,yy])

plt.plot(years,GrMB_JJA,label='JJA')
plt.plot(years,GrMB_JJAS,label='JJAS')
plt.plot(years,GrMB_ANN,label='Ann')
plt.title('Gr Mass Balance')
plt.ylabel('Gt')
plt.legend()


#%% NAO vs Gr MB statistics

x=NAO_JJA
y=GrMB_JJA
coefs=stats.pearsonr(x,y)
bx, mx = polyfit(x,y, 1)
print()
print('NAO JJA v Gr MB.')
print('correlation',"{:.3f}".format(coefs[0]))
print('confidence 1-p',"{:.4f}".format((1-coefs[1])))

x=NAO_JJAS
y=GrMB_JJAS
coefs=stats.pearsonr(x,y)
bx, mx = polyfit(x,y, 1)
print()
print('NAO JJAS v Gr MB.')
print('correlation',"{:.3f}".format(coefs[0]))
print('confidence 1-p',"{:.4f}".format((1-coefs[1])))

x=NAO_ANN
y=GrMB_ANN
coefs=stats.pearsonr(x,y)
bx, mx = polyfit(x,y, 1)
print()
print('NAO ANN v Gr MB.')
print('correlation',"{:.3f}".format(coefs[0]))
print('confidence 1-p',"{:.4f}".format((1-coefs[1])))

