import subprocess, socket, json, configparser, os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler


def syncGit():
    cmd = "cd /opt/MinerControl/app ;git pull origin master"
    subprocess.call(cmd, shell=True)

    return True



def getDate(worker_ip, worker_port, command):
    def linesplit(socket):
        buffer = socket.recv(4096).decode()
        done = False
        while not done:
            more = socket.recv(4096).decode()
            if not more:
                done = True
            else:
                buffer = buffer + more
        if buffer:
            return buffer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((worker_ip, int(worker_port)))
    if len(command) == 2:
        s.send(json.dumps({"command": command[0], "parameter": command[1]}))
    else:
        resp = s.send(json.dumps({"command": command[0]}).encode())

    # print(resp)
    response = linesplit(s)
    response = response.replace('\x00', '')
    response =response.replace('} {','},{')
    response = json.loads(response)
    s.close()
    return response


def getWorkers():
    with open('/opt/MinerControl/workers/workers.json') as json_file:
        data = json.load(json_file)
        return data


def pushData(metric, rig, worker, value, description):
    try:
        config = configparser.ConfigParser()
        config.read('/opt/MinerControl/config.ini')
        username = config['default']['username']
        secret = config['default']['secret']
        prometheusPushGW = config['default']['pushgateway_address']
        farm = config['default']['farm']
        zone = config['default']['zone']

        def auth_handler(url, method, timeout, headers, data):
            return basic_auth_handler(url, method, timeout, headers, data, username, secret)

        registry = CollectorRegistry()
        g = Gauge(metric, description, registry=registry,
                  labelnames=["username", "farm", "zone", "rig", "worker"] )
        g.labels(username=username, farm=farm, zone=zone, rig=rig, worker=worker).set(value)

        push_to_gateway(prometheusPushGW, job='batchA', registry=registry, handler=auth_handler)
        return True
    except:
        return False


def check_ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = 1
    else:
        pingstatus = 0

    return pingstatus
