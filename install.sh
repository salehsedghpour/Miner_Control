#!/bin/bash
cat << 'EOF'
.___  ___.  __  .__   __.  _______ .______           ______   ______   .__   __. .___________..______        ______    __
|   \/   | |  | |  \ |  | |   ____||   _  \         /      | /  __  \  |  \ |  | |           ||   _  \      /  __  \  |  |
|  \  /  | |  | |   \|  | |  |__   |  |_)  |       |  ,----'|  |  |  | |   \|  | `---|  |----`|  |_)  |    |  |  |  | |  |
|  |\/|  | |  | |  . `  | |   __|  |      /        |  |     |  |  |  | |  . `  |     |  |     |      /     |  |  |  | |  |
|  |  |  | |  | |  |\   | |  |____ |  |\  \----.   |  `----.|  `--'  | |  |\   |     |  |     |  |\  \----.|  `--'  | |  `----.
|__|  |__| |__| |__| \__| |_______|| _| `._____|    \______| \______/  |__| \__|     |__|     | _| `._____| \______/  |_______|

Miner-Control Team are working hard to monitor various brand of ASIC Miners.
Version: 1.0.0

EOF
if [ "$EUID" -ne 0 ]
  then echo "Please run the install.sh script with sudo:"
  echo "sudo bash install.sh"
  exit
fi
read -p "Please Enter your username: " username
echo "You have entered $username as your username"
read -p "Please Enter your Secret Key: " secret
echo "You have entered $secret as your Secret Key"
read -p "Please Enter your Farm name as you have entered in Miner-Control Dashboard: " farm
echo "You have entered $farm as your Farm name"
read -p "Please Enter your Zone Name as you have entered in Miner-Control Dashboard: " zone
echo "You have entered $zone as your Zone name"
mkdir /opt/MinerControl
echo "Creating config.ini"
echo '[default]' >> /opt/MinerControl/config.ini
echo "username = $username" >> /opt/MinerControl/config.ini
echo "secret = $secret" >> /opt/MinerControl/config.ini
echo "farm = $farm" >> /opt/MinerControl/config.ini
echo "zone = $zone" >> /opt/MinerControl/config.ini
echo "pushgateway_address = mon.hcsone.ir:19091" >> /opt/MinerControl/config.ini
apt update
apt upgrade -y
apt install python3.6 python3-pip git -y
mkdir /opt/MinerControl/app
mkdir /opt/MinerControl/worker
echo "http://$username:$secret@mon.hcsone.ir:8929" > /opt/MinerControl/.git-credentials



(cd /opt/MinerControl/app ;git init;git remote add origin "https://github.com/salehsedghpour/miner_control";git pull origin master)
pip3 install -r /opt/MinerControl/app/requirements.txt
(cd /opt/MinerControl/worker ;git init;git remote add origin "http://$username:$secret@mon.hcsone.ir:8929/$username/workers.git";git config --global user.email "$username@mon.hcsone.ir";git config --global user.name "$username";git config credential.helper store --file=/opt/MinerControl/.git-credentials)
chmod 777 /opt/MinerControl -R
chown $SUDO_USER:$SUDO_USER /opt/MinerControl -R
crontab -l > cronjob
echo "* * * * * python3 /opt/MinerControl/app/main.py" >> cronjob
echo "* * * * * python3 /opt/MinerControl/app/workerListUpdate.py" >> cronjob

crontab cronjob
rm cronjob


