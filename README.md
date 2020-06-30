# Herokidna

This is Herokidna, a robot inspired by two animals, an heron and an echidna. We built this robot as project for the *Robotics and Design* class at Politecnico di Milano.
The code we used is divided into five different files:
 - herokidna.py -> the heart of the robot, contains all the handlers for sensors and actuators, as well as its main algorithm to look for the pond and attack its enemies. It also contains the handler for the Telegram bot associated to the robot.
 - presentation.py -> a test file that can be used as a lighter version of the robot. Contains the same functions as Herokidna.py, but doesn't have the main algorithm. Can be used for testing.
 - add_wifi_from_usb.py -> file to be executed on boot, allows to pass information about new wifi connections from USB, so that the user doens't need to connect the board to an HDMI screen to do it
 - add_music_from_usb.py -> similar purpose as the previous file, it allows to pass new music to the robot to be used to convey emotions
 - boot_commands.txt -> after you execute "nano .bashrc" on your Raspberry, place these lines at the end of the file, to execute all the files on boot
 - instructions_for_spotify.txt -> follow these instructions to make your robot a remote speaker for Spotify (unfortunately our Raspberry had some issues and couldn't play sounds this way, but in general these instructions works fine)
 
If you're curious to find out more about our robot, check out this [video presentation](https://vimeo.com/433747450)!
