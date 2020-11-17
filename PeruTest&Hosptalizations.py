# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:27:27 2020

@author: admin
"""





###############################################################################
###############################################################################



dates = [
         '01052020.xlsx','02052020.xlsx','03052020.xlsx','04052020.xlsx','05052020.xlsx','06052020.xlsx','07052020.xlsx','08052020.xlsx','09052020.xlsx','10052020.xlsx',
         '11052020.xlsx','12052020.xlsx','13052020.xlsx','14052020.xlsx','15052020.xlsx','16052020.xlsx','17052020.xlsx','18052020.xlsx','19052020.xlsx','20052020.xlsx',
         '21052020.xlsx','22052020.xlsx','23052020.xlsx','24052020.xlsx','25052020.xlsx','26052020.xlsx','27052020.xlsx','28052020.xlsx','29052020.xlsx','30052020.xlsx','31052020.xlsx',
         '01062020.xlsx','02062020.xlsx','03062020.xlsx','04062020.xlsx','05062020.xlsx','06062020.xlsx','07062020.xlsx','08062020.xlsx','09062020.xlsx','10062020.xlsx',
         '11062020.xlsx','12062020.xlsx','13062020.xlsx','14062020.xlsx','15062020.xlsx','16062020.xlsx','17062020.xlsx','18062020.xlsx','19062020.xlsx','20062020.xlsx',
         '21062020.xlsx','22062020.xlsx','23062020.xlsx','24062020.xlsx','25062020.xlsx','26062020.xlsx','27062020.xlsx','28062020.xlsx','29062020.xlsx','30062020.xlsx',
         '01072020.xlsx','02072020.xlsx','03072020.xlsx','04072020.xlsx','05072020.xlsx','06072020.xlsx','07072020.xlsx','08072020.xlsx','09072020.xlsx','10072020.xlsx',
         '11072020.xlsx','12072020.xlsx','13072020.xlsx','14072020.xlsx','15072020.xlsx','16072020.xlsx','17072020.xlsx','18072020.xlsx','19072020.xlsx','20072020.xlsx',
         '21072020.xlsx','22072020.xlsx','23072020.xlsx','24072020.xlsx','25072020.xlsx','26072020.xlsx','27072020.xlsx','28072020.xlsx','29072020.xlsx','30072020.xlsx','31072020.xlsx',
         '01082020.xlsx','02082020.xlsx','03082020.xlsx','04082020.xlsx','05082020.xlsx','06082020.xlsx','07082020.xlsx','08082020.xlsx','09082020.xlsx','10082020.xlsx',
         '11082020.xlsx','12082020.xlsx','13082020.xlsx','14082020.xlsx','15082020.xlsx','16082020.xlsx','17082020.xlsx','18082020.xlsx','19082020.xlsx','20082020.xlsx',
         '21082020.xlsx','22082020.xlsx','23082020.xlsx','24082020.xlsx','25082020.xlsx','26082020.xlsx','27082020.xlsx','28082020.xlsx','29082020.xlsx','30082020.xlsx','31082020.xlsx',
         '01092020.xlsx','02092020.xlsx','03092020.xlsx','04092020.xlsx','05092020.xlsx','06092020.xlsx','07092020.xlsx','08092020.xlsx','09092020.xlsx','10092020.xlsx',
         '11092020.xlsx','12092020.xlsx','13092020.xlsx','14092020.xlsx','15092020.xlsx','16092020.xlsx','17092020.xlsx','18092020.xlsx','19092020.xlsx','20092020.xlsx',
         '21092020.xlsx','22092020.xlsx','23092020.xlsx','24092020.xlsx','25092020.xlsx','26092020.xlsx','27092020.xlsx','28092020.xlsx','29092020.xlsx','30092020.xlsx'
         '01102020.xlsx','02102020.xlsx','03102020.xlsx','04102020.xlsx','05102020.xlsx','06102020.xlsx','07102020.xlsx','08102020.xlsx','09102020.xlsx','10102020.xlsx',
         '11102020.xlsx','12102020.xlsx','13102020.xlsx','14102020.xlsx','15102020.xlsx','16102020.xlsx','17102020.xlsx','18102020.xlsx','19102020.xlsx','20102020.xlsx',
         '21102020.xlsx','22102020.xlsx','23102020.xlsx','24102020.xlsx','25102020.xlsx','26102020.xlsx','27102020.xlsx','28102020.xlsx','29102020.xlsx','30102020.xlsx','31102020.xlsx']         
         #fil = 'https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/POSITIVIDAD_'

def covid_peru(fil,dates):
    new_data = []
    
    for date in dates:
        file = fil + date
        try:
            temp = pd.read_excel(file)
            temp['date'] = date
            new_data.append(temp)
            print(date, ' FILE IMPORTED')
        except:
            print(date, ' FILE NO AVAILABLE')
            continue
    
    
    todos = pd.DataFrame()
    
    for each in new_data:
        try:
            todos = todos.append(each)
        except:
            continue
    
    return todos

def repl_date(df):
    df['date'] = df['date'].replace('.xlsx','',regex=True)
    df['date'] = pd.to_datetime(df['date'],format='%d%m%Y')
    return df


Peru_uci = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/UCI_',dates)
Peru_uci = Peru_uci.groupby('date').agg({'En Uso':sum,'Disponible':sum})
Peru_uci = Peru_uci.rename(columns={'En Uso':'UCI En Uso','Disponible':'UCI Disponible'}).reset_index()
Peru_uci = repl_date(Peru_uci)
#ok


Peru_hosp = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/HOSPITALIZADOS_',dates)
cond = Peru_hosp.loc[:,'CATEGORIA'] == 'USO DE VENTILACION MECÁNICA'
Peru_hosp.loc[cond,'CATEGORIA'] = Peru_hosp.loc[cond,'DETALLE']
cond = Peru_hosp.loc[:,'CATEGORIA'] == 'EVOLUCIÓN'
Peru_hosp.loc[cond,'CATEGORIA'] = Peru_hosp.loc[cond,'DETALLE']
Peru_hosp = Peru_hosp.drop('DETALLE',axis=1)
Peru_hosp = Peru_hosp.groupby(['CATEGORIA','date']).agg({'TOTAL':sum}).reset_index()
Peru_hosp['CATEGORIA']['CATEGORIA'] = Peru_hosp['CATEGORIA'].apply(lambda x : 'HOSP ' + x)
Peru_hosp = Peru_hosp.pivot(index='date',columns='CATEGORIA',values='TOTAL').reset_index()
Peru_hosp = repl_date(Peru_hosp)
#ok


Peru_casos = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/CASOS_',dates)
Peru_casos['Dpto'] = Peru_casos['Departamento'].where( Peru_casos['Región'].isna(), Peru_casos['Región'] )
Peru_casos['Dpto'] = Peru_casos['Dpto'].replace('LIMA METROPOLITANA','LIMA').replace('LIMA REGIÓN','LIMA')

Peru_casos = Peru_casos.drop(['PCR   (+)','PRUEBA RÁPIDA (+)','Pais','LETALIDAD (%)','Departamento','Región'],axis=1)

Peru_casos = Peru_casos.groupby(['Dpto','date']).sum().reset_index()

Peru_casos = repl_date(Peru_casos)
Peru_casos = Peru_casos.sort_values(['Dpto','date'])

Peru_casos2 = Peru_casos.loc[:,['TOTAL CASOS (+)','FALLECIDOS']].diff()
Peru_casos2 = Peru_casos2.rename(columns={'TOTAL CASOS (+)':'CASOS(dia)','FALLECIDOS':'FALLECIDOS(dia)'})


Peru_casos = pd.concat([Peru_casos, Peru_casos2], axis=1)


min_date = Peru_casos['date'].min()
temp = Peru_casos.loc[ Peru_casos.loc[:,'date']==min_date , ['TOTAL CASOS (+)','FALLECIDOS'] ]
Peru_casos.loc[ Peru_casos.loc[:,'date']==min_date , ['CASOS(dia)','FALLECIDOS(dia)'] ] = temp


del Peru_casos2, temp, min_date

#ok

Peru_posit = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/POSITIVIDAD_',dates)
Peru_posit['Dpto'] = Peru_posit['Departamento'].where( Peru_posit['REGION'].isna(), Peru_posit['REGION'] )
Peru_posit['Dpto'] = Peru_posit['Dpto'].replace('LIMA METROPOLITANA','LIMA').replace('LIMA REGIÓN','LIMA')

Peru_posit = Peru_posit.drop(['Pais','% de Positividad','Departamento','REGION'],axis=1)

Peru_posit = Peru_posit.groupby(['Dpto','date']).sum().reset_index()

Peru_posit = repl_date(Peru_posit)
Peru_posit = Peru_posit.sort_values(['Dpto','date'])

Peru_posit2 = Peru_posit.loc[:,['Muestras', 'Confirmado (+)']].diff()
Peru_posit2 = Peru_posit2.rename(columns={'Muestras':'Muestras(dia)','Confirmado (+)':'Confirmado(dia)'})

Peru_posit = pd.concat([Peru_posit, Peru_posit2], axis=1)


min_date = Peru_posit['date'].min()
temp = Peru_posit.loc[ Peru_posit.loc[:,'date']==min_date , ['Muestras','Confirmado (+)'] ]
Peru_posit.loc[ Peru_posit.loc[:,'date']==min_date , ['Muestras(dia)','Confirmado(dia)'] ] = temp


del Peru_posit2, temp, min_date


#list(Peru_posit.columns)
#list(Peru.columns)



Peru = pd.merge(Peru_casos,Peru_posit,on=['date','Dpto'])

Peru = pd.merge(Peru,Peru_uci,on=['date'])
Peru = pd.merge(Peru,Peru_hosp,on=['date'])

