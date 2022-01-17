import datetime
import geopy.distance
import time
from file_read_backwards import FileReadBackwards
import sys

x=float(sys.argv[1])#float(input('Please enter the Longitude of the accident(-10:0):'))--INSERT
y=float(sys.argv[2])#float(input('Plese enter the Latitude of the accident(45,51):'))--INSERT
origin=(x,y)
signal_range=float(sys.argv[3])#float(input('Please enter the signal range(unit:km):'))--INSERT
accident_date=sys.argv[4]+' '+sys.argv[5]#input('Plese enter the the date of the accident(d-m-Y H:M:S):').strip()--INSERT
a_day=int(accident_date.split(' ')[0].split('-')[0])
a_month=int(accident_date.split(' ')[0].split('-')[1])
a_year=int(accident_date.split(' ')[0].split('-')[2])
a_hour=int(accident_date.split(' ')[1].split(':')[0])
a_minute=int(accident_date.split(' ')[1].split(':')[1])
a_second=int(accident_date.split(' ')[1].split(':')[2])
accident_date=datetime.datetime(day=a_day,month=a_month,year=a_year,hour=a_hour,minute=a_minute,second=a_second)
linear_database=open('./linear_database.csv','w')
visited_ships_lines=[]
start_time=time.time()
insertion_time_list=[]
for line in open('./Data/nari_dynamic.csv','r'):
    line=line.strip()
    date=line.split(',')[3]
    day=int(date.split(' ')[0].split('-')[0])
    month=int(date.split(' ')[0].split('-')[1])
    year=int(date.split(' ')[0].split('-')[2])
    hour=int(date.split(' ')[1].split(':')[0])
    minute=int(date.split(' ')[1].split(':')[1])
    second=int(date.split(' ')[1].split(':')[2])
    current_date=datetime.datetime(day=day,month=month,year=year,hour=hour,minute=minute,second=second) 
    if current_date<=accident_date:
        insertion_start_time=time.time()
        linear_database.write(f'{line}\n')
        insertion_time_list.append(time.time()-insertion_start_time)
    else:
        linear_database.write(f'{line}\n')
        break
print(f'AVERAGE INSERTION TIME:{(sum(insertion_time_list)/len(insertion_time_list))}')
print(f'TOTAL CONSTRUCTION TIME:{time.time()-start_time}sec\n')
linear_database.close()
f=open('./linear_results.csv','w')
start_time=time.time()
visited_ships_id=[]
with FileReadBackwards("./linear_database.csv", encoding="utf-8") as frb:
    while True:
        line = frb.readline().strip()
        if not line:
            break
        if line.split(',')[0] not in visited_ships_id:
            visited_ships_id.append(line.split(',')[0])
            point=(float(line.split(',')[1]),float(line.split(',')[2]))
            if geopy.distance.distance(origin,point).km<=signal_range:
                f.write(f'{line}\n')
                f.flush()
end_time=time.time()
f.close()
print(f'TOTAL QUERY TIME:{end_time-start_time} sec\n')