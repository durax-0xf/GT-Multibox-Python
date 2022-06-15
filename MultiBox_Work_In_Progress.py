import shutil
import os
import subprocess
import wmi

print("How many instances of Growtopia to run: ")
count = int(input())

# get the username to locate DEFAULT Growtopia location
usr = os.environ['USERNAME']

# Growtopia location, self-explanatory
instances = 'C:\\Users\\' + usr + '\\AppData\\Local\\Growtopia\\'

#
source_hex = "47726f77746f706961" #-> Growtopia
modified_hex = "496e7374616e6365" #-> Instance

# shorthand
gt = "Growtopia.exe"

# hex address to growtopia - 47 72 6F 77 74 6F 70 69 61 -


# creates copies of the original Growtopia.exe file
# please note that the original file must be un-edited, with no hex modifications
# otherwise this whole system fails lol
for i in range(count):
    shutil.copy2("C:\\Users\\" + usr + "\\AppData\\Local\\Growtopia\\Growtopia.exe",
                 "C:\\Users\\" + usr + "\\AppData\\Local\\Growtopia\\Growtopia{}.exe".format(i))

dupes = -1  # literally no fucking clue why

# go through all files in growtopia folder
# ineffective, yet it does the job
for file in os.listdir(instances):

    if file.endswith(".exe") and file != gt:
        dupes += 1
        # turn regular strings into modified hex values
        # to add to hex indicating instance number
        ins = str(dupes).encode('utf-8')

        # read all hex values
        with open(instances + file, 'rb') as f:
            cont = f.read().hex()

        # replace the original hex with our modified hex
        cont = cont.replace(source_hex, modified_hex + ins.hex())

        # write the modified hex to the address
        with open(instances + file, 'wb') as g:
            g.write(bytes.fromhex(cont))

        # open modified copies of Growtopia
        os.chdir(instances)
        subprocess.Popen("Growtopia" + str(dupes) + ".exe")

print("Type `close` to close all running Growtopia instances and to remove residue files!")

if input() == "close":
    # current found Growtopia instances
    proc_name_gt = 0
    # go through all running processes to find Growtopia instances to terminate
    wMi = wmi.WMI()
    for process in wMi.Win32_Process():
        if "Growtopia" in process.name:
            print("Found " + process.name)
            # yes this is very slow. no I do not care, tried other solutions, didn't really work
            # thank you to: https://www.geeksforgeeks.org/how-to-terminate-a-running-process-on-windows-in-python/
            # method 2
            os.system('wmic process where name=' + '"%s"' % str(process.name) + ' delete')
            # convert Growtopia(n).exe -> "Growtopia(n).exe"
            # by using '"%s"' % growtopia process
            # thanks to this: https://stackoverflow.com/questions/11351043/enclose-a-variable-in-single-quotes-in-python
            proc_name_gt += 1

    # if no running Growtopia(n).exe instances are found
    if proc_name_gt == 0:
        print("NO GROWTOPIA PROCESSES FOUND! CRITICAL ERROR!")
        exit()

    # removes residue folders (such as Instance(n))
    for file in os.listdir('C:\\Users\\' + usr + '\\AppData\\Local\\'):
        if "Instance" in str(file):
            shutil.rmtree(r'C:\\Users\\' + usr + '\\AppData\\Local\\' + file)
            print("Removed: " + str(file) + " from " + 'C:\\Users\\' + usr + '\\AppData\\Local\\')

    # deletes all extra Growtopia(n).exe executables
    for file in os.listdir(instances):
        if file.endswith(".exe") and file != gt:
            os.remove(instances + file)
