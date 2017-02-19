#!/usr/bin/python

import psycopg2
import datetime

from psycopg2._psycopg import ProgrammingError

db1 = "DB1"
db2 = "DB2"
user = "postgres"
password = "1111"
host = "127.0.0.1"
port = "5432"

# flyTable = "fly_booking"
# hotelTable = "hotel_booking"
#
# fly_id = "id"
# fly_client_name = "client_name"
# fly_number = "fly_number"
# fly_from = "place_from"
# fly_to = "place_to"
# fly_date = "fly_date"
#
# hotel_id = "id"
# hotel_client_name = "client_name"
# hotel_name = "hotel_name"
# hotel_arrival = "arrival"
# hotel_departure = "departure"


def insert_records_2pc(client_name, place_from, place_to, hotel):
    tran_id = "insert"
    fly_conn = psycopg2.connect(database=db1, user=user, password=password, host=host, port=port)
    hotel_conn = psycopg2.connect(database=db2, user=user, password=password, host=host, port=port)
    print("Opened databases successfully")

    fly_xid = fly_conn.xid(42, tran_id, 'conn1')
    hotel_xid = hotel_conn.xid(42, tran_id, 'conn2')

    fly_conn.tpc_begin(fly_xid)
    hotel_conn.tpc_begin(hotel_xid)

    hotel_cur = hotel_conn.cursor()
    fly_cur = fly_conn.cursor()
    fly_cur.execute("show max_prepared_transactions;")
    rows = fly_cur.fetchall()
    print(rows)

    fly_cur.execute(
            "INSERT INTO fly_booking (client_name, fly_number, place_from, place_to, fly_date) "
            "VALUES ( %s, 32, %s, %s, now() )", (client_name, place_from, place_to))

    hotel_cur.execute(
            "INSERT INTO hotel_booking (client_name, hotel_name, arrival, departure) "
            "VALUES (%s, %s, now(), now() )", (client_name, hotel))

    fly_cur.close()
    hotel_cur.close()

    try:
        print("before prepare")
        fly_conn.tpc_prepare()
        hotel_conn.tpc_prepare()
        print("All prepared")
    except ProgrammingError:
        fly_conn.tpc_rollback()
        hotel_conn.tpc_rollback()
        print("All rollbacked")
    else:
        fly_conn.tpc_commit()
        hotel_conn.tpc_commit()
        print("All commited")

    fly_conn.close()
    hotel_conn.close()


i = datetime.datetime.now()
date = "'%s/%s/%s" % (i.day, i.month, i.year) + "'"

insert_records_2pc('Vitaliy', 'Kiev', 'Odessa', '5Ocean')
