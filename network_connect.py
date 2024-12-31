import network
import time
import json

saved_networks_file = "saved_networks.txt"

def connectToSSID(wlan, ssid, key):
    wlan.connect(ssid, key)
    time.sleep_ms(100)
    while (True):
        status = wlan.status()
        if status==network.STAT_CONNECTING:
            continue
        elif status==network.STAT_GOT_IP:
            print("Connected to %s" % ssid)
            break;
        else:
            print("Connection Failed")
            raise(OSError)
            break;

def checkSavedNetworks(wlan, scanned_networks):
    try:
        saved_networks_json = json.loads(open(saved_networks_file, 'r').read())
        for saved_network in saved_networks_json:
            for network in scanned_networks():
                print(saved_network['ssid'])
                print(saved_network['key'])
                if (network[0]==saved_network['ssid']) and (network[1]==saved_network['bssid']):
                    print("Found saved network: %s\nConnecting..."%network[0])
                    connectToSSID(wlan, network[0], saved_network['key'])
                    return 1
    except:
        return 0
    return 0

def promptWifiConfig(wlan, scanned_networks):
    print("Select Network: ")
    for idx,network in enumerate(scanned_networks):
        print("%d: %s" % (idx, network[0]))
    selected_network_idx = int(input(''))
    ssid = scanned_networks[selected_network_idx][0]
    bssid = scanned_networks[selected_network_idx][1]
    key = input("Enter password for %s:\n" % ssid)
    connectToSSID(wlan, ssid, key)
    try :
        saved_networks_json = json.loads(open(saved_networks_file, 'r').read())
    except :
        saved_networks_json = []
    saved_networks_json.append({'ssid':ssid, 'bssid':bssid, 'key':key})
    with open(saved_networks_file, "w") as f:
        json.dump(saved_networks_json, f)

def connectNetwork():
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    scanned_networks = wlan.scan()
    if (checkSavedNetworks(wlan, scanned_networks)):
        return wlan
    else :
        promptWifiConfig(wlan, scanned_networks)
        return wlan
