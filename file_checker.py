main_results=open('./main_results.csv','r')
linear_results=open('./linear_results.csv','r')

for linear_line in linear_results:
    main_results.seek(0,0)
    found=False
    for main_line in main_results:
        if linear_line.split(',')[0]==main_line.split(',')[0]:
            found=True
    if not found:
        print(linear_line)
