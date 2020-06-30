import os
import subprocess
import shutil

#Look for USB sticks
rpistr = "ls /media/pi"
proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
line = proc.stdout.readline()
if not line:
    exit(0)
    
#Check for a Music folder
device_name = line.rstrip().decode("utf-8")
rpistr = "ls /media/pi/" + device_name
proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)

newMusic = False
while True:
    line = proc.stdout.readline()
    if not line:
        break
    
    filename = line.rstrip().decode("utf-8")
    if filename == "Music":
        newMusic = True
        break
       
if not newMusic:
    exit(0)

#If music folder is present, check for new files
rpistr = "ls /media/pi/" + device_name + "/MusicEffects"
proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
music_names = ["Normal.mp3", "Attacking.mp3", "Drinking.mp3", "Eaten.mp3", "End.mp3"]
while True:
    line = proc.stdout.readline()
    if not line:
        break
    
    filename = line.rstrip().decode("utf-8")
    if filename in music_names:
        shutil.move(os.path.join("/media/pi/" + device_name + "/Music", filename), os.path.join("/home/pi/Herokidna/MusicEffects", filename))


        
exit(0)