import os, errno
from urllib.request import urlretrieve
from urllib.parse import quote

#retrieve and read an update manifest

BASE_URL = "https://never404.herokuapp.com/" #must end with slash

myf = open("output23.txt")
for line in myf:
    temp = line.split(maxsplit=1)
    if temp[0] == 'R': #hopefully this is the correct letter
            print('Deleting', temp[1].strip())
            try:
                os.remove(temp[1].strip())
            except:
                print('Unable to remove', temp[1].strip())
            try:
                if not os.listdir(os.path.dirname(temp[1].strip())): #https://thispointer.com/python-how-to-check-if-a-directory-is-empty/
                    os.rmdir(os.path.dirname(temp[1].strip()))
            except:
                pass
    elif temp[0] == 'M' or temp[0] == 'A':
            print('Path:', (os.path.dirname(temp[1].strip())))
            try:
                os.makedirs(os.path.dirname(temp[1].strip()))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            #end SO code
            #open(temp[1].strip(), 'a') #create the file if needed, automatically closed
            print('Downloading new/updated file:', temp[1].strip())
            try:
                urlretrieve(BASE_URL+temp[1], temp[1].strip())
            except:
                print('Unable to retrieve', temp[1].strip()+', continuing.')
myf.close()
