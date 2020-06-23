from functions import *
import json, configparser


def check_network(ip,rig,worker):
    network = check_ping(ip)
    pushData("network", rig, worker, network, "Checking Network Status")


def check_hashrate(hashrate,rig, worker):
    pushData("hash_rate2", rig, worker, hashrate, "Hash Rate Value")



syncGit()
#pushData("test_mamad", "bi rig", "bi worker", " bi value", "In dade faghat jahate test mibashad va hichgoone arzeshe digari nadarad")
with open('/opt/MinerControl/worker/workers.json') as json_file:
    data = json.load(json_file)
    for worker in data:
        config = configparser.ConfigParser()
        config.read('/opt/MinerControl/config.ini')
        farm = config['default']['farm']
        zone = config['default']['zone']
        if worker['farm'] == farm and worker['zone'] == zone:
            date = getDate(worker['ip'],worker['port'],[worker['commands']['monitoring']])


            hashrate = 10000
            temprature = 20
            #check_network(worker['ip'], worker['rig'], worker['name'])
            check_hashrate(hashrate, worker['rig'], worker['name'])
            pushData("temperature6",worker['rig'], worker['name'], temprature, "Temprature Value")
    json_file.close()
