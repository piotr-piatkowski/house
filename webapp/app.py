#!/usr/bin/env python
import time
from collections import defaultdict
from influxdb import InfluxDBClient

from flask import Flask, render_template
app = Flask(__name__)

conn = InfluxDBClient('172.22.22.1', 8086, 'idbup', 'idbup', 'house')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stove")
def stove():
    res = conn.query(
        'select mean(lower) as lower, mean(upper) as upper from temperature ' +
        'where time > now() - 24h group by time(1m)', epoch='ns')
    temps = res.get_points('temperature')
    points = defaultdict(list)
    for p in temps:
        ts = p['time'] / 1000000
        points['lower'].append([ts, p['lower']])
        points['upper'].append([ts, p['upper']])
    return render_template('stove.html', points=points)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
