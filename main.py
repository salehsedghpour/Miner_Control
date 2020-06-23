from functions import *
import json, configparser


def check_network(ip,rig,worker):
    network = check_ping(ip)
    pushData("network", rig, worker, network, "Checking Network Status")






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
            pushData("hash_rate", worker['rig'], worker['name'], hashrate, "Hash Rate Value")
            pushData("temperature",worker['rig'], worker['name'], temprature, "Temprature Value")
    json_file.close()
