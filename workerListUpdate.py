import subprocess

cmd = "cd /opt/MinerControl/worker ;git pull origin master"
subprocess.call(cmd, shell=True)