#! /usr/bin/python
import os
import xml.etree.cElementTree as et

from flask import Flask, render_template, request

app = Flask(__name__)


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
    gpx = et.Element("gpx", version="1.1", creator="Xcode")
    wpt = et.SubElement(gpx, "wpt", lat=lat, lon=lng)
    et.SubElement(wpt, "name").text = "location"
    et.ElementTree(gpx).write("location.gpx")

    os.system("osascript click_menu.applescript > /dev/null 2>&1")

    print("Updated lat: %s, lng: %s" % (lat, lng))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
