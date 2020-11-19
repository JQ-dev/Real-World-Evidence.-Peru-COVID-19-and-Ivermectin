# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:19:17 2020

@author: juanjchamie@gmail.com
"""

import pandas as pd
import numpy as np


version = '99'
path0 = 'C:/Users/admin/Downloads/Peru/Peru_deathsX_'+version+'.csv'

file1 = 'C:/Users/admin/Downloads/Peru/Data Peru/SINADEF_DATOS_ABIERTOS_08112020.csv'

file2 = 'C:/Users/admin/Downloads/Peru/Data Peru/positivos_covid.csv'
file3 = 'C:/Users/admin/Downloads/Peru/Data Peru/fallecidos_covid.csv'

#######################\
# Read from the path - It takes long because it is a excel file
fallecidosX = pd.read_csv(file1,engine='python')

del version, file1

fallecidos = fallecidosX.copy()

a = fallecidos['DEPARTAMENTO DOMICILIO'].apply(lambda x : '('+x[0:3]+')' )
fallecidos['PROVINCIA DOMICILIO'] = fallecidos['PROVINCIA DOMICILIO'] + a

#a = fallecidos['ESTADO CIVIL'].drop_duplicates()
#sum(fallecidos.loc[:,'EDAD'] != 'SIN REGISTRO')
#a = fallecidos[(fallecidos.loc[:,'EDAD'] == 'SIN REGISTRO')]


# Changing babies age from months to 0 ages
fallecidos.loc[ fallecidos['TIEMPO EDAD'] != 'AÑOS'  ,'EDAD'] = 0
fallecidos = fallecidos.drop(['TIEMPO EDAD'],axis=1)

fallecidos = fallecidos[(fallecidos.loc[:,'EDAD'] != 'SIN REGISTRO')]


#fallecidos.loc[fallecidos['ESTADO CIVIL']=='SEPARADO','EDAD'].mean()

# Rounding age
fallecidos['EDAD'] = fallecidos['EDAD'].astype(float)
fallecidos['EDAD'] = fallecidos['EDAD'].apply(lambda x : np.floor( x / 10 )*10 )
fallecidos.loc[ fallecidos.loc[:,'EDAD'] >= 80  ,'EDAD'] = 80


# Formatting date
fallecidos['FECHA'] = pd.to_datetime(fallecidos['FECHA'])

# Adding values without district
fallecidos = fallecidos.loc[:,('DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD')]
fallecidos['COUNT'] = 1

fallecidos = fallecidos.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD']).sum().reset_index()

# All ages
plus1 = fallecidos.loc[:].copy()
plus1.loc[:,'EDAD'] = 101
plus1 = plus1.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD']).sum().reset_index()


# Creating age groups <30 and >60
plus_60 = fallecidos[ fallecidos['EDAD'] > 59 ].copy()
plus_60.loc[:,'EDAD'] = 99
plus_60 = plus_60.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD']).sum().reset_index()

#plus_60.loc[:,'COUNT'].sum()
#fallecidos.loc[ fallecidos['EDAD'] > 59 ,'COUNT'].sum()

young_40 = fallecidos[ fallecidos['EDAD'] < 40 ].copy()
young_40.loc[:,'EDAD'] = 100
young_40 = young_40.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD']).sum().reset_index()

# Adding new age groups
fallecidos = fallecidos.append(plus1)
fallecidos = fallecidos.append(plus_60)
fallecidos = fallecidos.append(young_40)

#fallecidos['COUNT'].sum() ==plus1['COUNT'].sum()
#fallecidos.loc[ fallecidos['EDAD'] > 59 ,'COUNT'].sum() == plus_60['COUNT'].sum()
#fallecidos.loc[ fallecidos['EDAD'] < 40 ,'COUNT'].sum() == young_40['COUNT'].sum()
del plus1, plus_60, young_40


fallecidos['EDAD'] = fallecidos['EDAD'].apply(lambda x : str(x)[:-2])


# Adding total Departamento Deaths
fallecidos_d = fallecidos.groupby(['DEPARTAMENTO DOMICILIO','FECHA','EDAD']).sum().reset_index()
fallecidos_d['PROVINCIA DOMICILIO'] = 'Todas en ' + fallecidos_d['DEPARTAMENTO DOMICILIO']


# Adding total Country Deaths
fallecidos_c = fallecidos.groupby(['FECHA','EDAD']).sum().reset_index()
fallecidos_c['PROVINCIA DOMICILIO'] = 'Todas en Peru'
fallecidos_c['DEPARTAMENTO DOMICILIO'] = 'Todas en Peru'

#fallecidos['COUNT'].sum() == fallecidos_d['COUNT'].sum()

fallecidos = fallecidos.append(fallecidos_d)

fallecidos = fallecidos.append(fallecidos_c)

del fallecidos_d,fallecidos_c



#a = fallecidos.loc[fallecidos['COUNT']==489,'FECHA'].item()
#a = fallecidos.loc[fallecidos['FECHA']==a,:].copy()
#a = a.loc[a['DEPARTAMENTO DOMICILIO']=='LIMA',:].copy()
#a = a.loc[a['PROVINCIA DOMICILIO']=='Todas',:].copy()


# Population -
poblacion = pd.read_csv('C:/Users/admin/Downloads/Peru/Pobl Peru.csv',sep=',')
poblacion = poblacion.drop(['UB1','UB2','UBIGEO','DISTRITO','Mas de 60','Promedio'],axis=1)

# Removing districts
poblacion = poblacion.groupby(['DEPARTAMENTO','PROVINCIA']).sum().reset_index()


a = poblacion['DEPARTAMENTO'].apply(lambda x : '('+x[0:3]+')' )
poblacion['PROVINCIA'] = poblacion['PROVINCIA'] + a

# New age groups
poblacion['99'] = poblacion.loc[:,['60','70','80']].sum(axis=1)
poblacion['100'] = poblacion.loc[:,['0','10','20','30']].sum(axis=1)
poblacion = poblacion.rename(columns={'Total':'101'})

# Adding total Departamento Population
poblacion_d = poblacion.groupby(['DEPARTAMENTO']).sum().reset_index()
poblacion_d['PROVINCIA'] = 'Todas en ' + poblacion_d['DEPARTAMENTO']


# Adding total Country Population
poblacion_c = poblacion.sum()
poblacion_c[0],poblacion_c[1] = ['Todas en Peru','Todas en Peru']



poblacion = poblacion.append(poblacion_d)
poblacion = poblacion.append(poblacion_c, ignore_index=True)


#a = poblacion.loc[poblacion['DEPARTAMENTO']=='LIMA',:].copy()
#a = a.loc[a['PROVINCIA']=='Todas',:].copy()




poblacion = poblacion.melt(id_vars=['DEPARTAMENTO','PROVINCIA'], var_name='EDAD', value_name='Pobl')
poblacion.columns = ['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO','EDAD','POBL']




# Joining *****

fallecidos = pd.merge(fallecidos, poblacion, how='left',on=['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','EDAD'])


del poblacion_d , poblacion_c


#a = fallecidos.loc[fallecidos['COUNT']==489,'FECHA'].item()
#a = fallecidos.loc[fallecidos['FECHA']==a,:].copy()
#a = a.loc[a['DEPARTAMENTO DOMICILIO']=='LIMA',:].copy()
#a = a.loc[a['PROVINCIA DOMICILIO']=='Todas',:].copy()

###############################################################################
###############################################################################

df_casesX = pd.read_csv(file2,sep=';',engine='python')



# Reducing columns
df_cases = df_casesX.loc[:,['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']].copy()

a = df_cases['DEPARTAMENTO'].apply(lambda x : '('+x[0:3]+')' )
df_cases['PROVINCIA'] = df_cases['PROVINCIA'] + a


# Adding values without district
df_cases = df_cases.loc[:,('DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD')]
df_cases['CASES'] = 1

df_cases = df_cases.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()


#a = df_cases['EDAD'].drop_duplicates()

# Grouping Age
df_cases['EDAD'] = df_cases['EDAD'].apply(lambda x : np.floor( x / 10 )*10 )
df_cases.loc[ df_cases.loc[:,'EDAD'] >= 80  ,'EDAD'] = 80
df_cases = df_cases.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()


# Formatting date
df_cases['FECHA_RESULTADO'] = pd.to_datetime(df_cases['FECHA_RESULTADO'].astype(str), format='%Y%m%d')


#df_cases['CASES'].sum()

# Creating age groups all ages, <30 and >59
plus0 = df_cases.loc[:].copy()
plus0.loc[:,'EDAD'] = 101

plus60 = df_cases[ df_cases['EDAD'] > 59 ].copy()
plus60.loc[:,'EDAD'] = 99
plus60 = plus60.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()

young40 = df_cases[ df_cases['EDAD'] < 40 ].copy()
young40.loc[:,'EDAD'] = 100
young40 = young40.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()


#df_cases['CASES'].sum() ==plus0['CASES'].sum()
#df_cases.loc[ df_cases['EDAD'] > 59 ,'CASES'].sum() == plus60['CASES'].sum()
#df_cases.loc[ df_cases['EDAD'] < 40 ,'CASES'].sum() == young40['CASES'].sum()


# Adding new age groups
df_cases = df_cases.append(plus0)
df_cases = df_cases.append(plus60)
df_cases = df_cases.append(young40)

df_cases['EDAD'] = df_cases['EDAD'].apply(lambda x : str(x)[:-2])


del plus0, plus60, young40



# Adding total Departamento Population
df_cases_d = df_cases.groupby(['DEPARTAMENTO','FECHA_RESULTADO','EDAD']).sum().reset_index()
df_cases_d['PROVINCIA'] = 'Todas en ' + df_cases_d['DEPARTAMENTO']


# Adding total Country Population
df_cases_c = df_cases.groupby(['FECHA_RESULTADO','EDAD']).sum().reset_index()
df_cases_c['DEPARTAMENTO'] = 'Todas en Peru'
df_cases_c['PROVINCIA'] = 'Todas en Peru'

#df_cases['CASES'].sum() == df_cases_d['CASES'].sum()


df_cases = df_cases.append(df_cases_d)
df_cases = df_cases.append(df_cases_c)

df_cases.columns = ['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD','CASES']

del df_cases_d, df_cases_c


df_cases = pd.merge(df_cases, poblacion, how='left',on=['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','EDAD'])



#a = df_cases.loc[df_cases['CASES']==4020,'FECHA'].item()
#a = df_cases.loc[df_cases['FECHA']==a,:].copy()
#a = a.loc[a['DEPARTAMENTO DOMICILIO']=='LIMA',:].copy()
#a = a.loc[a['PROVINCIA DOMICILIO']=='Todas',:].copy()


#Peru_deaths_final = pd.merge(fallecidos, df_cases, how='outer',on=['FECHA','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','EDAD'])




###############################################################################
###############################################################################

df_deathsX = pd.read_csv(file3,sep=';',engine='python')

list(df_deathsX.columns)
# Reducing columns
df_deaths = df_deathsX.loc[:,('DEPARTAMENTO','PROVINCIA','FECHA_FALLECIMIENTO','EDAD_DECLARADA')].copy()
df_deaths.columns = ['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']

a = df_deaths['DEPARTAMENTO'].apply(lambda x : '('+x[0:3]+')' )
df_deaths['PROVINCIA'] = df_deaths['PROVINCIA'] + a

#a = df_deaths['EDAD'].drop_duplicates()

# Grouping Age
df_deaths['EDAD'] = df_deaths['EDAD'].apply(lambda x : np.floor( x / 10 )*10 )
df_deaths.loc[ df_deaths.loc[:,'EDAD'] >= 80  ,'EDAD'] = 80


# Formatting date
df_deaths['FECHA_RESULTADO'] = pd.to_datetime(df_deaths['FECHA_RESULTADO'].astype(str), format='%Y%m%d')



# Adding values without district
df_deaths = df_deaths.loc[:,('DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD')]
df_deaths['DEATHS'] = 1

df_deaths = df_deaths.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()


# Creating age groups <30 and >60
plus2 = df_deaths.loc[:].copy()
plus2.loc[:,'EDAD'] = 101

plus62 = df_deaths[ df_deaths['EDAD'] > 59 ].copy()
plus62.loc[:,'EDAD'] = 99
plus62 = plus62.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()

young42 = df_deaths[ df_deaths['EDAD'] < 40 ].copy()
young42.loc[:,'EDAD'] = 100
young42 = young42.groupby(['DEPARTAMENTO','PROVINCIA','FECHA_RESULTADO','EDAD']).sum().reset_index()


#df_deaths['DEATHS'].sum() == plus2['DEATHS'].sum()
#df_deaths.loc[ df_deaths['EDAD'] > 59 ,'DEATHS'].sum() == plus62['DEATHS'].sum()
#df_deaths.loc[ df_deaths['EDAD'] < 40 ,'DEATHS'].sum() == young42['DEATHS'].sum()

# Adding new age groups
df_deaths = df_deaths.append(plus2)
df_deaths = df_deaths.append(plus62)
df_deaths = df_deaths.append(young42)

df_deaths['EDAD'] = df_deaths['EDAD'].apply(lambda x : str(x)[:-2])


del plus2, plus62, young42


# Adding total Departamento Population
df_deaths_d = df_deaths.groupby(['DEPARTAMENTO','FECHA_RESULTADO','EDAD']).sum().reset_index()
df_deaths_d['PROVINCIA'] = 'Todas en ' + df_deaths_d['DEPARTAMENTO']

# Adding total Country Population
df_deaths_c = df_deaths.groupby(['FECHA_RESULTADO','EDAD']).sum().reset_index()
df_deaths_c['DEPARTAMENTO'] = 'Todas en Peru'
df_deaths_c['PROVINCIA'] = 'Todas en Peru'


df_deaths = df_deaths.append(df_deaths_d)
df_deaths = df_deaths.append(df_deaths_c)


del df_deaths_d, df_deaths_c

df_deaths.columns = ['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA','EDAD','DEATHS']

df_deaths = pd.merge(df_deaths, poblacion, how='left',on=['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','EDAD'])




Peru_deaths_final = pd.concat([df_cases,df_deaths,fallecidos])

Peru_deaths_final.columns = ['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'FECHA', 'EDAD',
         'Casos COVID','Pobl', 'Muertes COVID','cuenta']

Peru_deaths_final = Peru_deaths_final.fillna(0)

#################################################################################


Peru_norm = Peru_deaths_final[Peru_deaths_final['EDAD']=='99'].copy()


#################################################################################

Peru_deaths_final.to_csv(path0,index=False)


del Peru_deaths_final, a, df_cases, df_casesX, df_deaths, df_deathsX
del  fallecidosX, path0, poblacion


#################################################################################
Peru_norm2 = Peru_norm.copy()
Peru_norm = Peru_norm2.copy()

cond =  Peru_norm['PROVINCIA DOMICILIO'].apply(lambda x : "Todas en" in x )
Peru_norm = Peru_norm[cond]

cond =  Peru_norm['PROVINCIA DOMICILIO'].apply(lambda x : "Todas en Peru" not in x )
Peru_norm = Peru_norm[cond]

#deptos = Peru_norm['DEPARTAMENTO DOMICILIO'].drop_duplicates()
deptos = ['UCAYALI','TUMBES','PIURA','MOQUEGUA','LORETO','LIMA','LA LIBERTAD','CUSCO','AREQUIPA']
cond =  Peru_norm['DEPARTAMENTO DOMICILIO'].apply(lambda x : x in deptos )
Peru_norm = Peru_norm[cond]


Peru_norm = Peru_norm.drop(['PROVINCIA DOMICILIO','EDAD'],axis=1)



Peru_norm = Peru_norm.groupby('DEPARTAMENTO DOMICILIO','FECHA')










