with open('testFile.txt', 'wb') as f:
    f.seek(1024*1024) 
    f.write('0'.encode())
