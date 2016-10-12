#! /usr/bin/python
import os
import argparse
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

    # ignore positions during writing location file
    if not lock.locked():
        gpx_gen(lat, lng)

    return "OK"


def gpx_gen(lat, lng):
    with lock:
        with open('location.gpx', 'w') as location:
            location.write('<gpx><wpt lat="%s" lon="%s"></wpt></gpx>' % (lat, lng))

        os.system('osascript update.applescript >/dev/null 2>&1')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', help='open browser', action='store_true', default=False)
    args = parser.parse_args()

    if args.open:
        os.system('open "http://localhost:5000"')


if __name__ == '__main__':
    main()
    app.run(threaded=True, debug=False)
