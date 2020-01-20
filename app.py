#coding: utf-8

import time
import sqlite3
from flask import Flask, request
from .bme280 import BME280

app = Flask(__name__)

@app.route('/view', methods=["GET"])
def view():
    return "ok"

@app.route('/', methods=["POST"])
def post():
    bme280 = BME280()
    post_data = request.get_data().splitlines()
    post_data = list(map(lambda x: int(x), post_data))
    ijid = post_data[0]
    calib = post_data[1:1+32]
    data = post_data[1+32:1+32+8]
    bme280 = BME280()
    bme280.setCalib(calib)
    bme280.setData(data)
    db_insert(ijid, bme280.T, bme280.P, bme280.H)
    print("T: %0.2f, P: %0.2f, H: %0.2f" % (bme280.T, bme280.P, bme280.H))
    return 'ok'

def db_init():
    db = sqlite3.connect('data.db')
    sql = u"""
        CREATE TABLE IF NOT EXISTS t_log (
            id integer primary key,
            ijid integer,
            measured_at timestmap,
            t numeric,
            p numeric,
            h numeric
        );
    """
    db.execute(sql)
    db.close()

def db_insert(ijid, t, p, h):
    db = sqlite3.connect('data.db')
    db.execute(
        "INSERT INTO t_log (ijid, measured_at, t, p, h) VALUES (?, ?, ?, ?, ?);",
        (
            ijid,
            time.time(),
            t,
            p,
            h
        ))
    db.commit()
    db.close()

db_init()
if __name__ == '__main__':
    app.run()