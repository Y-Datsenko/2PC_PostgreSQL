#!/usr/bin/python

import psycopg2
import datetime

db1 = "DB1"
db2 = "DB2"
user = "postgres"
password = "1111"
host = "127.0.0.1"
port = "5432"

flyTable = "fly_booking"
hotelTable = "hotel_booking"

fly_id = "id"
fly_client_name = "client_name"
fly_number = "fly_number"
fly_from = "place_from"
fly_to = "place_to"
fly_date = "fly_date"

hotel_id = "id"
hotel_clent_name = "client_name"
hotel_name = "hotel_name"
hotel_arrival = "arrival"
hotel_departure = "daparture"

fly_conn = psycopg2.connect(database=db1, user=user, password=password, host=host, port=port)
hotel_conn = psycopg2.connect(database=db2, user=user, password=password, host=host, port=port)

print("Opened databases successfully")

fly_cur = fly_conn.cursor()
hotel_cur = hotel_conn.cursor()

i = datetime.datetime.now()
date = "'%s/%s/%s" % (i.day, i.month, i.year)+"'"

fly_cur.execute("INSERT INTO fly_booking (id, client_name, fly_number, place_from, place_to, fly_date) VALUES (3, 'Paul', 32, 'California', 'Kiev', now() )");
fly_conn.commit()
print("Fly record created successfully")

hotel_cur.execute("INSERT INTO hotel_booking (id, client_name, hotel_name, arrival, departure) VALUES (2, 'Paul', 'Plaza', now(), now() )");
hotel_conn.commit()
print("Hotel record created successfully")

fly_conn.close()
hotel_conn.close()



# cur.execute("SELECT id, name, address, salary  from COMPANY")
# rows = cur.fetchall()
# for row in rows:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3], "\n")

# print ("Operation done successfully")
# conn.close()

def insertFlyInfo(fly_cur, id) :
	print(id)
