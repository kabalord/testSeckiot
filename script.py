import time
import random
import requests
import json
import pandas as pd
from ipaddress import IPv4Address

def random_ip_address(seed):
    random.seed(seed)
    return str(IPv4Address(random.getrandbits(32)))

temps = int(time.strftime('%S',time.localtime()))
adresse = pd.DataFrame(dtype=str)
if __name__ == '__main__':
    i = 0 #parcours d'address
    j = 0 #compte les nombres de requetes envoyes au serveur
    while adresse.shape[0] < 10:
        t = int(time.strftime('%S',time.localtime()))
        if t == temps + 60:
            print("Temps écoulé !",i,"adresse générée")
            break
        else:
            dirip = random.random()
            peticion = random_ip_address(dirip)
            url = 'http://ip-api.com/json/'+str(peticion)+'?fields=timezone,mobile,proxy,hosting'
            response = requests.get(url, params=peticion)
            j = j+1
            if response.status_code == 200 and j < 45:
                response_json = json.loads(response.text)
                if bool(response_json) == True:
                    adresse.loc[i, "IPV4"] = peticion
                    adresse.loc[i, "timezone"] = response_json['timezone']
                    adresse.loc[i, "mobile"] = response_json['mobile']
                    adresse.loc[i, "proxy"] = response_json['proxy']
                    adresse.loc[i, "hosting"] = response_json['hosting']
                    i = i+1
                    time.sleep(1)
print(adresse)
print(j)