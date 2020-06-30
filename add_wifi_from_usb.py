import os
import subprocess
import pygame
import time

def add_wifi(wifi_name, wifi_pass):
    config_lines = [
         '\n',
         'network={',
         '\tssid="{}"'.format(wifi_name),
         '\tpsk="{}"'.format(wifi_pass),
         '\tkey_mgmt=WPA-PSK',
         '}'
    ]
    config = '\n'.join(config_lines)
    print(config)
    
    with open("/etc/wpa_supplicant/wpa_supplicant.conf","a+") as wifi:
        wifi.write(config)
    
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/MusicEffects/Applause.mp3")
    pygame.mixer.music.play()
    time.sleep(10)

#Look for USB sticks
rpistr = "ls /media/pi"
proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
line = proc.stdout.readline()
if not line:
    exit(0)

#Read the files inside the USB stick
device_name = line.rstrip().decode("utf-8")
rpistr = "ls /media/pi/" + device_name
proc = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
while True:
    line = proc.stdout.readline()
    if not line:
        break
    
    filename = line.rstrip().decode("utf-8")
    if filename == "wifi.txt":
        f = open("/media/pi/" + device_name + "/wifi.txt","r")
        wifi_name = f.readline().rstrip()
        wifi_pass = f.readline()
        add_wifi(wifi_name, wifi_pass)
        
exit(0)