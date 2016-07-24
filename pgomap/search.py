#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import math
import time

from pgoapi import PGoApi
from pgoapi.utilities import f2i, get_cellid
from pgomap import config
from .models import parse_map

logger = logging.getLogger(__name__)

TIMESTAMP = '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'
REQ_SLEEP = 1

api = PGoApi()


def send_map_request(api, position):
    try:
        api.set_position(*position)
        api.get_map_objects(latitude=f2i(position[0]),
                            longitude=f2i(position[1]),
                            since_timestamp_ms=TIMESTAMP,
                            cell_id=get_cellid(position[0], position[1]))
        return api.call()
    except Exception as e:
        logger.warn("Uncaught exception when downloading map %s" % e)
        return False


def login(pos):
    logger.info('Attempting login to Pokemon Go.')

    if config['USERNAME'] and config['PASSWORD']:
        api.set_position(*pos)
        while not api.login(config['AUTH_SERVICE'], config['USERNAME'], config['PASSWORD']):
            logger.info('Failed to login to Pokemon Go. Trying again.')
            time.sleep(REQ_SLEEP)
        logger.info('Login to Pokemon Go successful.')


def check_login(pos):
    if api._auth_provider and api._auth_provider._ticket_expire:
        remaining_time = api._auth_provider._ticket_expire / 1000 - time.time()

        if remaining_time > 60:
            logger.info("Skipping Pokemon Go login process since already logged in for another {:.2f} seconds"
                        .format(remaining_time))
        else:
            login(pos)
    else:
        login(pos)


lat_gap_meters = 150
lng_gap_meters = 86.6
meters_per_degree = 111111
lat_gap_degrees = float(lat_gap_meters) / meters_per_degree


def calculate_lng_degrees(lat):
    return float(lng_gap_meters) / (meters_per_degree * math.cos(math.radians(lat)))


def generate_location_steps(pos, steps):
    ring = 1  # Which ring are we on, 0 = center
    lat = pos[0]
    lng = pos[1]

    yield (pos[0], pos[1], 0)  # Middle circle

    while ring < steps:
        lat += lat_gap_degrees
        lng -= calculate_lng_degrees(lat)

        for direction in range(6):
            for i in range(ring):
                if direction == 0:  # Right
                    lng += calculate_lng_degrees(lat) * 2

                if direction == 1:  # Right Down
                    lat -= lat_gap_degrees
                    lng += calculate_lng_degrees(lat)

                if direction == 2:  # Left Down
                    lat -= lat_gap_degrees
                    lng -= calculate_lng_degrees(lat)

                if direction == 3:  # Left
                    lng -= calculate_lng_degrees(lat) * 2

                if direction == 4:  # Left Up
                    lat += lat_gap_degrees
                    lng -= calculate_lng_degrees(lat)

                if direction == 5:  # Right Up
                    lat += lat_gap_degrees
                    lng += calculate_lng_degrees(lat)

                yield (lat, lng, 0)  # Middle circle

        ring += 1


def search(lat, lng):
    position = (lat, lng, 0)
    check_login(position)

    for step_location in generate_location_steps(position, config['STEPS']):
        logger.debug('Scan location {:f}, {:f}'.format(step_location[0], step_location[1]))

        res = send_map_request(api, step_location)
        try:
            parse_map(res)
        except KeyError:
            logger.error('Scan step failed. Response dictionary key error.')

        time.sleep(REQ_SLEEP)
