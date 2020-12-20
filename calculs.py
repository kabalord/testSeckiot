import datetime
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
      CREATE TABLE IF NOT EXISTS calculs (
      id int(11) NOT NULL AUTO_INCREMENT,
      indexation DATETIME NOT NULL,
      timezone_principal varchar(100) DEFAULT NULL,
      mobile_mean varchar(100) NOT NULL,
      proxy_mean varchar(100) NOT NULL,
      hosting_mean varchar(100) NOT NULL,
      PRIMARY KEY (id)
      );
    
"""
cursor.execute(sql)

#récupération des champs table ipv4
cursor.execute("""SELECT timezone, mobile, proxy, hosting FROM ipv4 ORDER BY id DESC LIMIT 100;""")
rows = cursor.fetchall()

#calcule des moyennes 
timezone_principal = ""
mobile_mean = 0
proxy_mean = 0
hosting_mean = 0

for row in rows:
   #print('{0} : {1} - {2} - {3}'.format(row[0], row[1], row[2], row[3]))
   if row[1] == '1':
       mobile_mean += 1
   if row[2] == '1':
       proxy_mean += 1
   if row[3] == '1':
       hosting_mean += 1    

#récupération de timezone plus répresentative    
cursor.execute(""" SELECT timezone, COUNT(timezone) AS tz FROM ipv4 GROUP BY timezone ORDER BY tz DESC LIMIT 1 """)   
rows = cursor.fetchall()


indexation = datetime.datetime.now()
result = (indexation, rows[0][0], str(mobile_mean) + '%', str(proxy_mean) + '%', str(hosting_mean) + '%')
cursor.execute("""INSERT INTO calculs(indexation, timezone_principal, mobile_mean, proxy_mean, hosting_mean) VALUES (%s, %s, %s, %s, %s)""", result)
conn.commit()
conn.close()

print(result)