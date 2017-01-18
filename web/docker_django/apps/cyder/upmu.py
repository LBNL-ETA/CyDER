from __future__ import division
import models as m
import datetime as dt
import tool as t


def get(location, datetime):
    date_from = dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    date_to = "False"
    cmd = "ssh cyder@bt-eplus.dhcp.lbl.gov python CyDER/web/docker_django/worker/upmu/get.py 2016-12-15_12:00:00 2016-12-15_12:02:00"
    pass
