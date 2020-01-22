#coding: utf-8

import os
import time
import sqlite3
from flask import Flask, request
import ambient

from .bme280 import BME280

app = Flask(__name__)

@app.route('/view', methods=["GET"])
def view():
    return "ok"

@app.route('/bme280', methods=["POST"])
def bme280():
    post_data = request.get_data().splitlines()
    channel = post_data[0].strip()
    writekey = post_data[1].strip()
    post_data = list(map(lambda x: int(x), post_data[2:]))
    calib = post_data[0:32]
    data = post_data[32:32+8]
    bm = BME280()
    bm.setCalib(calib)
    bm.setData(data)
    app.logger.info("channel: %s, T: %0.2f, P: %0.2f, H: %0.2f" % (channel, bm.T, bm.P, bm.H))
    db_insert(channel, bm.T, bm.P, bm.H)
    am = ambient.Ambient(channel, writekey)
    am.send({'d1': bm.T, 'd2': bm.P, 'd3': bm.H})
    return 'ok'

@app.route('/', methods=["POST"])
def post():
    post_data = request.get_data().splitlines()
    post_data = list(map(lambda x: int(x), post_data))
    ijid = post_data[0]
    calib = post_data[1:1+32]
    data = post_data[1+32:1+32+8]
    bme280 = BME280()
    bme280.setCalib(calib)
    bme280.setData(data)
    app.logger.info("T: %0.2f, P: %0.2f, H: %0.2f" % (bme280.T, bme280.P, bme280.H))
    db_insert2(ijid, bme280.T, bme280.P, bme280.H)
    am = ambient.Ambient(os.environ['AM_CHANNEL'], os.environ['AM_WRITE_KEY'])
    am.send({'d1': bme280.T, 'd2': bme280.P, 'd3': bme280.H})
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
    sql = u"""
        CREATE TABLE IF NOT EXISTS t_bme280 (
            id integer primary key,
            channel varchar,
            measured_at timestmap,
            t numeric,
            p numeric,
            h numeric
        );
    """
    db.execute(sql)
    db.close()

def db_insert(channel, t, p, h):
    db = sqlite3.connect('data.db')
    db.execute(
        "INSERT INTO t_bme280 (channel, measured_at, t, p, h) VALUES (?, ?, ?, ?, ?);",
        (
            channel,
            time.time(),
            t,
            p,
            h
        ))
    db.commit()
    db.close()

def db_insert2(ijid, t, p, h):
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
