# TODO




#Comands to use to find disk sector size
#Windows:fsutil fsinfo ntfsinfo c:
#Linux:fdisk -l | grep "Sector size"
#Average 512 bytes

import math

from pandas.tseries.offsets import YearEnd
from DBMS import *
import os
import datetime
#INITIALIZE
    #INSERT AFTER TESTING
# sector_size=input('Please enter sector size(deafault:512 bytes):')
# if sector_size=='':
#     sector_size=512
# else:
#     sector_size=int(sector_size)
# x_low=float(input('Please enter the lower x-value:'))
# y_low=float(input('Please enter the lower y-value:'))
# width=float(input('Please enter the width:'))
# height=float(input('Please enter the height:'))
# max_leaf_size=math.floor(47/sector_size)
    #REMOVE AFTER TESTING


for file in os.listdir('./Data_Blocks/'):
    os.remove('Data_Blocks/'+file)


######----------FINAL
x_low=-10.0
y_low=45.0
width=10
height=6
sector_size=input('Please enter the sector size(default:512 bytes):')
if sector_size=='':
    sector_size=512
else:
    sector_size=int(sector_size)
max_leaf_size=6#math.floor(47/sector_size)
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
######----------FINAL


# for item in os.listdir('./Data_Blocks/'):

#     os.remove('./Data_Blocks/'+item)


    #INSERT AFTER TESTING
# doomed_ship=input('Wich ship to DESTROY:')
# kill_date_time=input('At what date and time(d-m-Y H:M:S):')
# signal_range=input('Please enter the signal range:')
# for line in open('./Test_Data/Test.csv','r').readlines():#PUT WHEN DONE TESTING ./Data/nari_dynamic.csv
#     line=line.strip()
#     id=line.split(',')[0]
#     date_time=line.split(',')[3]
#     if id==doomed_ship and date_time==kill_date_time:
#         Quad_Tree.rangeQuery(float(line.split(',')[1]),float(line.split(',')[2]),signal_range,float(line.split(',')[1])-signal_range,float(line.split(',')[2])-signal_range,signal_range*2,signal_range*2,Quad_Tree.root)
#         break
#     else:
#         Quad_Tree.insert(id,float(line.split(',')[1],float(line.split(',')[2],date_time)))
    
# for i in Quad_Tree.range_query_results:
#     print(i.strip())

# for line in open('./Test_data/Test.csv','r').readlines():
#     line=line.strip()
#     Quad_Tree.insert(line.split(',')[0],float(line.split(',')[1]),float(line.split(',')[2]),line.split(',')[3])
# Quad_Tree.rangeQuery(-5,48,110,-6,47,2,2,Quad_Tree.root)
# print('RESULTS:')
# for line in Quad_Tree.range_query_results:
#     print(line.strip())