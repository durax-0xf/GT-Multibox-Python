import shutil
import os
import subprocess
import time



print("gt instances: ")
count = int(input())

usr = os.environ['USERNAME']
instances = 'C:\\Users\\' + usr + '\\AppData\\Local\\Growtopia\\'
source_hex = "47726f77746f706961"
modified_hex = "496e7374616e6365"
gt = "Growtopia.exe"

# hex address to growtopia - 47 72 6F 77 74 6F 70 69 61 -



# makes gt copies
for i in range(count):
    shutil.copy2("C:\\Users\\" + usr + "\\AppData\\Local\\Growtopia\\Growtopia.exe",
                 "C:\\Users\\" + usr + "\\AppData\\Local\\Growtopia\\Growtopia{}.exe".format(i))

dupes = -1 # literally no fucking clue why
opengts = []
for file in os.listdir(instances):
    
    if file.endswith(".exe") and file != gt:
        dupes+=1
        ins = str(dupes).encode('utf-8')  # convert to instance number

        with open(instances + file, 'rb') as f:
            cont = f.read().hex()

        cont = cont.replace(source_hex, modified_hex + ins.hex())  # replace name with modified hex

        with open(instances + file, 'wb') as g:
            g.write(bytes.fromhex(cont))

        os.chdir(instances)
        subprocess.Popen("Growtopia"+str(dupes)+".exe")
        opengts.append("Growtopia"+str(dupes)+".exe")

print("Type `clear` to remove residue files. Must close all GT's first")
if(input()=="clear"):
    
    for file in os.listdir('C:\\Users\\' + usr + '\\AppData\\Local\\'): # clear all residue folders
        if "Instance" in str(file):
            shutil.rmtree(r'C:\\Users\\' + usr + '\\AppData\\Local\\'+file)
            print(str(file))
            
    for file in os.listdir(instances): #del all extra gts
        if file.endswith(".exe") and file!= gt:
            os.remove(instances+file)
