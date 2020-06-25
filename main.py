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
            #if date != False:
            try:
                hashrate = float(date['STATS'][1]['GHS 5s'])
                temprature = float(date['STATS'][1]['temp6'])
                pushData("hash_rate", worker['rig'], worker['name'], hashrate, "Hash Rate Value")
                pushData("temperature",worker['rig'], worker['name'], temprature, "Temprature Value")
            except:
                hashrate = 100
                temprature = date['STATS'][1]['temp6']
                pushData("hash_rate", worker['rig'], worker['name'], hashrate, "Hash Rate Value")
                pushData("temperature", worker['rig'], worker['name'], temprature, "Temprature Value")
            #else:
            #    hashrate = 0
            #    temprature = 2
                # check_network(worker['ip'], worker['rig'], worker['name'])
            #    pushData("hashrate", worker['rig'], worker['name'], hashrate, "Hash Rate Value")
            #    pushData("temperature", worker['rig'], worker['name'], temprature, "Temprature Value")
    json_file.close()
