for i in range(4):
    fn="100MB"
    with open(fn+str(i)+'.txt', 'wb') as f:
        f.seek(1024*1024*100) 
        f.write('0'.encode())

for i in range(10):
    fn="100MB"
    with open(fn+str(i)+'.txt', 'wb') as f:
        f.seek(1024*1024*10) 
        f.write('0'.encode())

for i in range(30):
    fn="100MB"
    with open(fn+str(i)+'.txt', 'wb') as f:
        f.seek(1024*1024) 
        f.write('0'.encode())

for i in range(100):
    fn="100MB"
    with open(fn+str(i)+'.txt', 'wb') as f:
        f.seek(1024*500) 
        f.write('0'.encode())

for i in range(1000):
    fn="100MB"
    with open(fn+str(i)+'.txt', 'wb') as f:
        f.seek(1024*100) 
        f.write('0'.encode())


#100kb -100MB

#total < 12GB

##NOT Exact cuz IM using 1KB = 1000MB for this scratch math

#4 100MB == 1GB
#10 10MBs ==  100MB
#30 1MBs == 30MBs
#100 500KBs == 50MBSs
#1000 100KBs == 100MBs



