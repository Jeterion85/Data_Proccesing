#Comands to use to find disk sector size
#Windows:fsutil fsinfo ntfsinfo c:
#Linux:fdisk -l | grep "Sector size"
#Average 512 bytes
from pandas.tseries.offsets import YearEnd
from DBMS import *
import os
import datetime
import math


for file in os.listdir('./Data_Blocks/'):
    os.remove('Data_Blocks/'+file)


x_low=-10.0
y_low=45.0
width=10
height=6
sector_size=input('Please enter the sector size(default:512 bytes):')
if sector_size=='':
    sector_size=512
else:
    sector_size=int(sector_size)
max_leaf_size=math.floor(47/sector_size)
Quad_Tree(x_low,y_low,width,height,max_leaf_size)
Hash_Index()
x=float(input('Please enter the Longitude of the accident(-10:0):'))
y=float(input('Plese enter the Latitude of the accident(45,51):'))
signal_range=float(input('Please enter the signal range(unit:km):'))
accident_date=input('Plese enter the the date of the accident(d-m-Y H:M:S):').strip()
a_day=int(accident_date.split(' ')[0].split('-')[0])
a_month=int(accident_date.split(' ')[0].split('-')[1])
a_year=int(accident_date.split(' ')[0].split('-')[2])
a_hour=int(accident_date.split(' ')[1].split(':')[0])
a_minute=int(accident_date.split(' ')[1].split(':')[1])
a_second=int(accident_date.split(' ')[1].split(':')[2])
accident_date=datetime.datetime(day=a_day,month=a_month,year=a_year,hour=a_hour,minute=a_minute,second=a_second)
for line in open('./Test_data/Test.csv','r').readlines():
    date=line.split(',')[3]
    day=int(date.split(' ')[0].split('-')[0])
    month=int(date.split(' ')[0].split('-')[1])
    year=int(date.split(' ')[0].split('-')[2])
    hour=int(date.split(' ')[1].split(':')[0])
    minute=int(date.split(' ')[1].split(':')[1])
    second=int(date.split(' ')[1].split(':')[2])
    current_date=datetime.datetime(day=day,month=month,year=year,hour=hour,minute=minute,second=second)
    if current_date>accident_date:
        line=line.strip()
        Quad_Tree.insert(line.split(',')[0],float(line.split(',')[1]),float(line.split(',')[2]),line.split(',')[3])      
        x_r_MBR=x-360*signal_range*10**3/40075000
        y_r_MBR=y-360*signal_range*10**3/40075000
        width=2*abs(x-x_r_MBR)
        height=2*abs(y-y_r_MBR)
        Quad_Tree.rangeQuery(x,y,signal_range,x_r_MBR,y_r_MBR,width,height,Quad_Tree.root)
        break
    else:
        line=line.strip()
        Quad_Tree.insert(line.split(',')[0],float(line.split(',')[1]),float(line.split(',')[2]),line.split(',')[3])
for result in Quad_Tree.range_query_results:
    print(result.strip())
