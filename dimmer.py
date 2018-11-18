#!/usr/bin/env python2
import ephem
import logging
from datetime import datetime, time

class Dimmer(object):
    def __init__(self, scheduler):
        self._observer = ephem.Observer()
        self._observer.pressure = 0
        self._observer.horizon = '-6'
        self._observer.lat = '38.262469'
        self._observer.lon = '-85.648625'

        self.brightness = 100

        self.update()

        # Run every 5 minutes
        scheduler.add_job(self.update, 'cron', minute='*/5')

    def update(self):
        now = datetime.now()
        now_time = now.time()
        
        self._observer.date = ephem.now()

        morning = self._observer.next_rising(ephem.Sun(), use_center=True)
        night = self._observer.next_setting(ephem.Sun(), use_center=True)

        if now_time >= time(6,5) and now_time <= time(19,30):
        #if morning < night:
            # Morning is sooner, so it must be night
            logging.info("It daytime time")
            self.brightness = 80
        else:
            logging.info("It is night time")
            self.brightness = 10
