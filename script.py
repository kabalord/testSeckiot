import time
import random
import requests
import json
import pandas as pd
from ipaddress import IPv4Address

# =============================================================================
# GENERATION DES ADRESSES IPsV4
# =============================================================================
def random_ip_address(seed):
    random.seed(seed)
    return str(IPv4Address(random.getrandbits(32)))

temps = int(time.strftime('%S',time.localtime()))
adresse = pd.DataFrame(dtype=str)
if __name__ == '__main__':
    i = 0
    j = 0
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
                    time.sleep(3)

# =============================================================================
#AJOUT A LA BD
# =============================================================================
import mysql.connector
conn = mysql.connector.connect(host="localhost",
                                user="root", password="root",
                                port="8889",
                                database="seckiot")
cursor = conn.cursor()

#Creation table
sql = """
   DROP TABLE IF EXISTS ipv4;
   CREATE TABLE IF NOT EXISTS ipv4 (
      id int(11) NOT NULL AUTO_INCREMENT,
      ip varchar(100) NOT NULL,
      timezone varchar(100) DEFAULT NULL,
      mobile varchar(100) NOT NULL,
      proxy varchar(100) NOT NULL,
      hosting varchar(100) NOT NULL,
      PRIMARY KEY (id),
      UNIQUE KEY ip (ip)
      );
"""
cursor.execute(sql, multi=True)

for a in range(0,adresse.shape[0]):
    donnee = (adresse.loc[a, "IPV4"],adresse.loc[a, "timezone"],
              adresse.loc[a, "mobile"],adresse.loc[a, "proxy"],adresse.loc[a, "hosting"])
    cursor.execute("""INSERT INTO ipv4 (ip, timezone, mobile, proxy, hosting) VALUES(%s, %s, %s, %s, %s)""", donnee)

conn.close()