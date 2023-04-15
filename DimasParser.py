
#----------------------ШАГ0. Зашли на страничку со всеми сегодняшними матчами
import requests
from bs4 import BeautifulSoup
result = requests.get("http://www.tennisexplorer.com/matches/?type=all&year=2021&month=12&day=7")
#result = requests.get("http://www.tennisexplorer.com/match-detail/?id=2007904")
src = result.content
soup = BeautifulSoup(src, 'lxml')


#----------------------ШАГ1. Забрали ссылки на странички всех сегодняшних матчей
#print([tag.find("a")["href"] for tag in soup.select("td:has(a)")])
todays_list=[qwe.text.strip() for qwe in soup.select('a[href*="/match-detail/?id="]')]
links=[]
for q in soup.select('a[href*="/match-detail/?id="]'):
    links.append(q['href'])

todays_list=list(zip(todays_list, links))

todays_list_=[]
for idx, item in enumerate(todays_list):
    if todays_list[idx][0]=='info':
        #В todays_list_ забираем только вторую колонку изначального списка todays_list_
        todays_list_.append(todays_list[idx][1])
len(todays_list_)
todays_list_



#----------------------ШАГ2. Заходим по очереди на каждую страничку матча, проходящего сегодня
#ОБРАЗЕЦ result = requests.get("http://www.tennisexplorer.com/match-detail/?id=2007904")
get_link= "http://www.tennisexplorer.com" + todays_list_[0]
#get_link= "http://www.tennisexplorer.com/match-detail/?id=2007904"
result = requests.get(get_link)
src = result.content
soup = BeautifulSoup(src, 'lxml')



print(get_link)




import pandas as pd
import numpy as np

#1й способ
soup.select('th[class="plName"]')
#имена забрали со странички матча
lst=[qwe.text.strip() for qwe in soup.select('th[class="plName"]')]
np_lst = np.array(lst)

lst_=np.reshape(np_lst, (1, 2))
df = pd.DataFrame(lst_, columns=["p1", "p2"])
df



#----------------------ШАГ3. За остальным идём по очереди на персональную страничку каждого из участников матча
links=[]

req= soup.find_all("th", {"class":"plName"})
type(req)
links=[]
for w in req:
    #неправильно
    #links.append(w.get('href'))
        #надо так
        #links.append(w.find('a')['href'])
    #или так
    links.append(w.a.get('href'))
        #или так
        #rows = req.findAll("td")
        #linkelement = rows[linkpos]
        #a_element = linkelement.find('a')
        #a_element.get('href')
links


import re
get_player= "http://www.tennisexplorer.com" + links[0]
result_ = requests.get(get_player)
src_ = result_.content
soup_ = BeautifulSoup(src_, 'lxml')
#columns = soup_.findAll('div', text = re.compile('Age'), attrs = {'class' : 'date'})
#[qwe.text.strip() for qwe in columns]
columns=soup_.findAll('div', {'class' : 'date'})
len([qwe.text.strip() for qwe in columns])
lst_p1=[qwe.text.strip() for qwe in soup_.select('div[class="date"]')]

get_player= "http://www.tennisexplorer.com" + links[1]
result_ = requests.get(get_player)
src_ = result_.content
soup_ = BeautifulSoup(src_, 'lxml')
lst_p2=[qwe.text.strip() for qwe in soup_.select('div[class="date"]')]


def podstava(new_col, like, list):
    for i in range(len(list)):
        if (like in list[i]):
            df[new_col]=list[i][list[i].find(':')+2:]
            break
        else:
            df[new_col]='-'

podstava('Country_p1', 'Countr', lst_p1)
podstava('Sgl_rank_p1', 'singles', lst_p1)
podstava('Age_p1', 'Age', lst_p1)
podstava('Dbl_rank_p1', 'doubles', lst_p1)
podstava('Hand_p1', 'Plays', lst_p1)

podstava('Country_p2', 'Countr', lst_p2)
podstava('Sgl_rank_p2', 'singles', lst_p2)
podstava('Age_p2', 'Age', lst_p2)
podstava('Dbl_rank_p2', 'doubles', lst_p2)
podstava('Hand_p2', 'Plays', lst_p2)
df



#----------------------ШАГ4. Возвращаемся на страничку с матчем. Кол-во побед/проигрышей за всю карьеру по каждому из игроков (Career - Player1, Career - Player2) суммарно
#----------------------это не делал...и на каждом из покрытий отдельно.
print("TOTAL career (w/l):",end=' ')
wl_total=[qwe.text.strip() for qwe in soup.select('a[href$="?annual=all"]')]
print(wl_total)
#----------------------+ Кол-во побед/проигрышей в 2021 по каждому из игроков (Career - Player1, Career - Player2) суммарно
print("2021 career (w/l):",end=' ')
wl_2021=[qwe.text.strip() for qwe in soup.select('a[href*="?annual=2021"]')]
print(wl_2021)



def wl(i):
    df['W_p'+str(i+1)]=int(wl_total[i][:wl_total[i].find('/')])
    df['L_p'+str(i+1)]=int(wl_total[i][wl_total[i].find('/')+1:])
    
wl(0)
wl(1)
df



#----------------------ШАГ5. Котировки на матч
try:
    s= [qwe.text.strip() for qwe in soup.select_one('.average').findAll('div', {'class' : 'odds-in'})]
    df['coeff'] = s[0] + ' vs ' + s[1]
except:
    df['coeff'] = 'no coeff'

df


#----------------------ШАГ6. Детальные резульатты последних матчей каждого
#----------------------матчи 1го соперника
pl1=soup.findAll('div', {'class' : 'half-l'})
for w in pl1:
    s=w.findAll('td', {'class' : 'score'})
#---общий счёт 10 последних матчей
score_p1=[qwe.text.strip() for qwe in s]
#---детальный счёт 10 последних матчей
scores_p1=[]
for w in s:
    scores_p1.append(w.a.get('title'))

#---список участников матчей
for w in pl1:
    s=w.findAll('td', {'class' : 'tl'})
participants_p1=[]
for w in s:
    if "/player/" in w.a.get('href'):
        links = w.find_all('a', href=True)
        participants_p1.append([qwe.text.strip() for qwe in links])
        ss=w.find_all(attrs={"class": "notU"} ,href=True)
        for i in ss:
            p1=i.attrs["href"]
p1=p1[p1.find('/',2)+1:-1]

        
#----------------------матчи 2го соперника
pl2=soup.findAll('div', {'class' : 'half-r'})
for w in pl2:
    s=w.findAll('td', {'class' : 'score'})
#---общий счёт 10 последних матчей
score_p2=[qwe.text.strip() for qwe in s]
#---детальный счёт 10 последних матчей
scores_p2=[]
for w in s:
    scores_p2.append(w.a.get('title'))


#---список участников матчей
for w in pl2:
    s=w.findAll('td', {'class' : 'tl'})
participants_p2=[]
for w in s:
    if "/player/" in w.a.get('href'):
        links = w.find_all('a', href=True)
        participants_p2.append([qwe.text.strip() for qwe in links])
        ss=w.find_all(attrs={"class": "notU"} ,href=True)
        #---фамилии участников для сортировки
        for i in ss:
            p2=i.attrs["href"]
p2=p2[p2.find('/',2)+1:-1]

print(score_p1)
print(scores_p1)
print(participants_p1)
print(score_p2)
print(scores_p2)
print(participants_p2)



#----------------------ШАГ7. Косвенный рейтинг соперников по опыту (кол-во сыгранных матчей)
for w in pl1:
    s=w.findAll('td', {'class' : 'score'})

#---ИГРОК1. общая стата его соперников в 10 прошлых матчах
for w in pl1:
    s=w.findAll('td', {'class' : 'tl'})
links_p1=[]
for w in s:
    if "/player/" in w.a.get('href'):
        ss=w.find_all(attrs={"class": ""} ,href=True)
        for i in ss:
            links_p1.append(i.attrs["href"])
links_p1
    
#---ИГРОК2. общая стата его соперников в 10 прошлых матчах
for w in pl2:
    s=w.findAll('td', {'class' : 'tl'})
links_p2=[]
for w in s:
    if "/player/" in w.a.get('href'):
        ss=w.find_all(attrs={"class": ""} ,href=True)
        for i in ss:
            links_p2.append(i.attrs["href"])
links_p2

print(links_p1)
print(chr(13))
print(links_p2)
print(chr(13))




dff=pd.DataFrame(participants_p1,columns =['p1','p2'])
dff['sets']=score_p1
dff['games']=scores_p1
dff['alignment by']=p1
dff[['set_p1','set_p2']] = dff["sets"].str.split(":", n = 1, expand = True)
dff[['s1p1_g','s1p2_g','s2p1_g','s2p2_g','s3p1_g','s3p2_g']]  = dff["games"].str.split("/|;|_|%|-|,",expand=True)
dff=dff.fillna(0)
    #ищет скобки...факультативно
    #dff.apply(lambda col: col.str.contains("\(", na=False), axis=1)
def mochi_skobki(col):
    list=dff[col]
    for i in range(len(list)):
        if str(list[i]).find('(')==True:
            list[i]=str(list[i])[:str(list[i]).find('(')]
    dff[col]=list
mochi_skobki('s1p1_g')
mochi_skobki('s1p2_g')
mochi_skobki('s2p1_g')
mochi_skobki('s2p2_g')
mochi_skobki('s3p1_g')
mochi_skobki('s3p2_g')

for index in range(dff.shape[0]):
    if dff.loc[index, 'p1'].lower() != dff.loc[index, 'alignment by']:
        dff.loc[index,['p1','p2']] = dff.loc[index,['p2','p1']].values
        dff.loc[index,['set_p1','set_p2']] = dff.loc[index,['set_p2','set_p1']].values
        dff.loc[index,['s1p1_g','s1p2_g']] = dff.loc[index,['s1p2_g','s1p1_g']].values
        dff.loc[index,['s2p1_g','s2p2_g']] = dff.loc[index,['s2p2_g','s2p1_g']].values
        dff.loc[index,['s3p1_g','s3p2_g']] = dff.loc[index,['s3p2_g','s3p1_g']].values
dff


#------применяем собранное к Игроку1
rival_p1_gamerk=[]
rival_p1_rating=[]

for idx in range(len(links_p1)):

    get_link= "http://www.tennisexplorer.com" + links_p1[idx]
    result = requests.get(get_link)
    src = result.content
    soup_p1 = BeautifulSoup(src, 'lxml')

    #----------------------rival_p1_gamerk
    rival_p1_gamerk.append([qwe.text.strip() for qwe in soup_p1.select('a[href$="?annual=all"]')])
    #----------------------rival_p1_rating

    #columns=soup_p1.findAll('div', {'class' : 'date'})
    #len([qwe.text.strip() for qwe in columns])
    rival_p1=[qwe.text.strip() for qwe in soup_p1.select('div[class="date"]')]
    for i in range(len(rival_p1)):
        fl=False
        if ('singles' in rival_p1[i]):
            fl=True
            rival_p1_rating.append(rival_p1[i][rival_p1[i].find(':')+2:])
            break
    if fl==False:
        rival_p1_rating.append('-')

dff['rival_p1_gamerk']=rival_p1_gamerk
dff['rival_p1_rating']=rival_p1_rating
dff



d=pd.DataFrame(participants_p2,columns =['p1','p2'])
d['sets']=score_p2
d['games']=scores_p2
d['alignment by']=p2
d[['set_p1','set_p2']] = d["sets"].str.split(":", n = 1, expand = True)
d[['s1p1_g','s1p2_g','s2p1_g','s2p2_g','s3p1_g','s3p2_g']]  = d["games"].str.split("/|;|_|%|-|,",expand=True)
d=d.fillna(0)
    #ищет скобки...факультативно
    #d.apply(lambda col: col.str.contains("\(", na=False), axis=1)
def mochi_skobki(col):
    list=d[col]
    for i in range(len(list)):
        if str(list[i]).find('(')==True:
            list[i]=str(list[i])[:str(list[i]).find('(')]
    d[col]=list
mochi_skobki('s1p1_g')
mochi_skobki('s1p2_g')
mochi_skobki('s2p1_g')
mochi_skobki('s2p2_g')
mochi_skobki('s3p1_g')
mochi_skobki('s3p2_g')

for index in range(d.shape[0]):
    if d.loc[index, 'p1'].lower() != d.loc[index, 'alignment by']:
        d.loc[index,['p1','p2']] = d.loc[index,['p2','p1']].values
        d.loc[index,['set_p1','set_p2']] = d.loc[index,['set_p2','set_p1']].values
        d.loc[index,['s1p1_g','s1p2_g']] = d.loc[index,['s1p2_g','s1p1_g']].values
        d.loc[index,['s2p1_g','s2p2_g']] = d.loc[index,['s2p2_g','s2p1_g']].values
        d.loc[index,['s3p1_g','s3p2_g']] = d.loc[index,['s3p2_g','s3p1_g']].values
d


#------применяем собранное к Игроку1
rival_p1_gamerk=[]
rival_p1_rating=[]

for idx in range(len(links_p1)):

    get_link= "http://www.tennisexplorer.com" + links_p2[idx]
    result = requests.get(get_link)
    src = result.content
    soup_p1 = BeautifulSoup(src, 'lxml')

    #----------------------rival_p1_gamerk
    rival_p1_gamerk.append([qwe.text.strip() for qwe in soup_p1.select('a[href$="?annual=all"]')])
    #----------------------rival_p1_rating

    #columns=soup_p1.findAll('div', {'class' : 'date'})
    #len([qwe.text.strip() for qwe in columns])
    rival_p1=[qwe.text.strip() for qwe in soup_p1.select('div[class="date"]')]
    for i in range(len(rival_p1)):
        fl=False
        if ('singles' in rival_p1[i]):
            fl=True
            rival_p1_rating.append(rival_p1[i][rival_p1[i].find(':')+2:])
            break
    if fl==False:
        rival_p1_rating.append('-')

d['rival_p1_gamerk']=rival_p1_gamerk
d['rival_p1_rating']=rival_p1_rating
d
