#! /usr/bin/python
import os
from threading import Lock

from flask import Flask, render_template, request

app = Flask(__name__)
lock = Lock()


@app.route('/')
def poke_map():
    return render_template('map.html')


@app.route('/pos')
def get_pos():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    gpx_gen(lat, lng)

    return "OK"


def gpx_gen(lat, lng):
    with lock:
        with open('location.gpx', 'w') as location:
            location.write('<gpx><wpt lat="%s" lon="%s"></wpt></gpx>' % (lat, lng))

        os.system('osascript click_menu.applescript >/dev/null 2>&1')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
