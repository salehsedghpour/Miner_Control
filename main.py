from functions import *
import json, configparser


def check_network(ip,rig,worker):
    network = check_ping(ip)
    pushData("network", rig, worker, network, "Checking Network Status")


def check_hashrate(hashrate,rig, worker):
    pushData("hash_rate", rig, worker, hashrate, "Hash Rate Value")


def check_temprature(temprature, rig, worker):
    pushData("temprature", rig, worker, temprature, "Temprature Value")

with open('/opt/MinerControl/worker/workers.json') as json_file:
    data = json.load(json_file)
    for worker in data:
        config = configparser.ConfigParser()
        config.read('../config.ini')
        farm = config['default']['farm']
        zone = config['default']['zone']
        if worker['farm'] == farm and worker['zone'] == zone:
            date = getDate(worker['ip'],worker['port'],worker['commands']['monitoring'])
            hashrate = data['STATS'][1]['GHS 5s']
            temprature = data['STATS'][1]['temp2']
            check_network(worker['ip'], worker['rig'], worker['name'])
            check_hashrate(hashrate, worker['rig'], worker['name'])
            check_temprature(temprature, worker['rig'], worker['name'])