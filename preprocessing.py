from datetime import datetime
data=open('/home/george/Documents/nari_dynamic.csv','r')
data_1=open('./Data/nari_dynamic.csv','w')
i=True
for line in data:
    if i:
        i=not i
        continue
    line=line.strip()
    date=datetime.utcfromtimestamp(int(line.split(',')[8])).strftime('%d-%m-%Y %H:%M:%S')
    data_1.write(line.split(',')[0]+','+line.split(',')[6]+','+line.split(',')[7]+','+date+'\n')
    data_1.flush()  
data.close()
data_1.close()
