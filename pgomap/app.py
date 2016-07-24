#!/usr/bin/python
# -*- coding: utf-8 -*-

import calendar
import os
from datetime import datetime
from threading import Lock

from flask import Flask, jsonify, render_template, request
from flask.json import JSONEncoder

from pgomap.search import search
from .models import Pokemon

etc_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'etc')
gpx_path = os.path.join(etc_dir, 'location.gpx')
as_path = os.path.join(etc_dir, 'update.applescript')


class Pgomap(Flask):
    def __init__(self, import_name, **kwargs):
        super(Pgomap, self).__init__(import_name, **kwargs)
        self.json_encoder = CustomJSONEncoder
        self.lock = Lock()
        self.route("/", methods=['GET'])(self.poke_map)
        self.route("/pos", methods=['GET'])(self.get_pos)

    def poke_map(self):
        return render_template('map.html')

    def get_pos(self):
        d = {}
        lat = request.args.get('lat')
        lng = request.args.get('lng')

        # ignore positions during writing location file
        if not self.lock.locked():
            d = self.gpx_gen(lat, lng)

        return jsonify(d)

    def gpx_gen(self, lat, lng):
        with self.lock:
            with open(gpx_path, 'wb') as location:
                location.write('<gpx><wpt lat="%s" lon="%s"></wpt></gpx>' % (lat, lng))

            os.system('osascript %s >/dev/null 2>&1' % as_path)

            # scan nearby while moving
            search(float(lat), float(lng))
            return {'pokemons': Pokemon.get_active()}


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset():
                    obj = obj - obj.utcoffset()
                return int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
