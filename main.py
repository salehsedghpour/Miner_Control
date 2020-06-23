from functions import *
import json, configparser


def check_network(ip,rig,worker):
    network = check_ping(ip)
    pushData("network", rig, worker, network, "Checking Network Status")


def check_hashrate(hashrate,rig, worker):
    pushData("hash_rate", rig, worker, int(float(hashrate)), "Hash Rate Value")


def check_temprature(temprature, rig, worker):
    pushData("temperature", rig, worker, temprature, "Temprature Value")

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

            hashrate = date['STATS'][1]['GHS 5s']
            temprature = date['STATS'][1]['temp6']
            #check_network(worker['ip'], worker['rig'], worker['name'])
            check_hashrate(int(float(hashrate)), worker['rig'], worker['name'])
            check_temprature(temprature, worker['rig'], worker['name'])