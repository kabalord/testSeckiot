import random
import requests
import json

from ipaddress import IPv4Address

dirip = random.random()

def random_ip_address(seed):

    random.seed(seed)

    return str(IPv4Address(random.getrandbits(32)))

peticion = random_ip_address(dirip)
print(peticion)
if __name__ == '__main__':
    url = 'http://ip-api.com/json/'+str(peticion)+'?fields=timezone,mobile,proxy,hosting'
    response = requests.get(url, params=peticion)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        timezone = response_json['timezone']
        mobile = response_json['mobile']
        proxy = response_json['proxy']
        hosting = response_json['hosting']
        print(timezone)
        print(mobile)
        print(proxy)
        print(hosting)




#Exemple d'appel : random_ip_address(10) => 146.71.112.211