#!/bin/sh
VENV_PYTHON="/home/neptuniam/.local/share/virtualenvs/Dribbble-Crawler-gSUpCBJG"
PROJECT="/mnt/c/Users/LJone/OneDrive/Desktop/Programs/Dribbble-Crawler"
SCRIPT="main.py"
cd "${PROJECT}" && "${VENV_PYTHON}" "${SCRIPT}"

/home/neptuniam/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/mnt/c/Program Files (x86)/Intel/Intel(R) Management Engine Components/iCLS:/mnt/c/Program Files/Intel/Intel(R) Management Engine Components/iCLS:/mnt/c/Windows/System32:/mnt/c/Windows:/mnt/c/Windows/System32/wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/Program Files/Intel/WiFi/bin:/mnt/c/Program Files/Common Files/Intel/WirelessCommon:/mnt/c/Program Files (x86)/Intel/Intel(R) Management Engine Components/DAL:/mnt/c/Program Files/Intel/Intel(R) Management Engine Components/DAL:/mnt/c/Program Files (x86)/Intel/Intel(R) Management Engine Components/IPT:/mnt/c/Program Files/Intel/Intel(R) Management Engine Components/IPT:/mnt/c/Users/LJone/OneDrive/Desktop/Programs:/mnt/c/Windows/System32:/mnt/c/Windows:/mnt/c/Windows/System32/wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0:/mnt/c/Windows/System32/OpenSSH:/mnt/c/Program Files (x86)/nodejs:/mnt/c/Program Files/Git/cmd:/mnt/c/Users/LJone/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/LJone/AppData/Local/atom/bin:/mnt/c/Users/LJone/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/LJone/AppData/Roaming/npm:/snap/bin

* * * * * cd /mnt/c/Users/LJone/OneDrive/Desktop/Programs/Dribbble-Crawler/ && pipenv run python3 main.py > log 2>&1
* * * * * cd /mnt/c/Users/LJone/OneDrive/Desktop/Programs/Dribbble-Crawler && whoami > cronfile
