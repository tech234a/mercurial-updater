import os, errno, json
from urllib.request import urlretrieve
from urllib.parse import quote
import requests
from progress_meter import withprogress, MeterWindow #https://bitbucket.org/takluyver/progress_meter/

def fakeprint(*argv): #https://www.geeksforgeeks.org/args-kwargs-python/
    pass

#GUI Code Adapted from https://geektechstuff.com/2018/12/07/creating-a-progress-bar-python/
#retrieve and read an update manifest
from tkinter import *
# ttk makes the window look like running Operating System’s theme
from tkinter import ttk
# create root tkinter window to hold progress bar
root = Tk()
root.resizable(False, False) #https://stackoverflow.com/a/37447917/
# create progress bar
progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 600)
# pack progress bar into root
progress.pack()



#Make config file

config = json.load(open('updaterconfig.json', 'rb'))

VERBOSE = config['VERBOSE']
if not VERBOSE: print = fakeprint

INSTALLED_VERSION = config['INSTALLED_VERSION'] #1
print("Installed version:", INSTALLED_VERSION)

CHANNEL = config['CHANNEL'] #"stable"



BASE_MANIFEST_URL = config['BASE_MANIFEST_URL'] #"https://raw.githubusercontent.com/tech234a/flashpoint-manifests/master/"
BASE_FILE_URL = config['BASE_FILE_URL'] #"https://never404.herokuapp.com/" #must end with slash
#End make config file

TARGET_VERSION = int(requests.get(BASE_MANIFEST_URL + CHANNEL + ".txt").text.strip())
print("Target version:", TARGET_VERSION)

actions = {}



for i in range(INSTALLED_VERSION, TARGET_VERSION+1):
    #add manifest retrieval printing
    myf = requests.get(BASE_MANIFEST_URL + str(i) + ".txt").text.strip().split('\n')#open("output23.txt")
    for item in myf:
        temp = item.split(maxsplit=1) #split by spaces
        actions[str(temp[1])] = str(temp[0])
        #print(actions)

TOTAL_COUNT = len(actions)

# to step progress bar up
progress.config(mode = 'determinate', maximum=TOTAL_COUNT, value = 0)
root.update()
#progress.step(5)

#@withprogress(TOTAL_COUNT, color="green")
#def rundl(actions):
    #print("in here")
completed_count = 0
error_count = 0
errors = []
for fileaction in actions:
    #print("in loop")
    error = False
    statusinfo = "[" + str(format(round((completed_count/TOTAL_COUNT)*100, 2), ".2f")) + "%] [" + str(completed_count) + "/" + str(TOTAL_COUNT) + "]: " #https://stackoverflow.com/a/20457115/
    if actions[fileaction] == 'R': #hopefully this is the correct letter
            print(statusinfo + 'Deleting', fileaction.strip())
            try:
                os.remove(fileaction.strip())
            except:
                print('ERROR: Unable to remove', fileaction.strip())
                error = True
            try:
                if not os.listdir(os.path.dirname(fileaction.strip())): #https://thispointer.com/python-how-to-check-if-a-directory-is-empty/
                    os.rmdir(os.path.dirname(fileaction.strip()))
            except:
                pass
    elif actions[fileaction] == 'M' or actions[fileaction] == 'A':
            #print('Path:', (os.path.dirname(fileaction.strip())))
            try:
                os.makedirs(os.path.dirname(fileaction.strip()))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            #end SO code
            #open(fileaction.strip(), 'a') #create the file if needed, automatically closed
            print(statusinfo + 'Downloading new/updated file:', fileaction.strip())
            try:
                urlretrieve(BASE_FILE_URL+quote(fileaction, safe='\/'), fileaction.strip())
            except:
                print('ERROR: Unable to retrieve', fileaction.strip()+', continuing.')
                error = True
                #raise
    if error:
        errors += fileaction
        error_count += 1
    completed_count += 1
    progress.step(1)
    root.title(statusinfo[:-2]+" Updating Flashpoint...")
    root.update_idletasks()
    root.update()
    #meter.set(completed_count)
    #bar(completed_count)
        #return completed_count, error_count, errors

#bar = InitBar(title='Downloading and Installing Flashpoint Update', size=TOTAL_COUNT)
#print('down here!')
#completed_count, error_count, errors = rundl(actions)

print("Completed", completed_count, "files.")
if error_count: print("Of these files,", error_count, "files contain errors and were not downloaded correctly. These files are:\n", errors)





config['INSTALLED_VERSION'] = TARGET_VERSION
json.dump(config, open('updaterconfig.json', 'wb'))
#myf.close()
