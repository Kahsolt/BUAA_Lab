#!/usr/bin/env python

import os
import time
import random
import subprocess32
import requests
import rospy
from ros_rt_control.srv import *
from std_msgs.msg import String

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROG_BASE = os.path.join(BASE_DIR, 'programs')
LOG = os.path.join(BASE_DIR, 'log', 'out')

DOWN_RATE = 0.1
prog_start_time = None
cur_program = None
cur_process = None
pub = None


def switch_program(prog):
    global cur_program, cur_process, prog_start_time

    if cur_program == prog:
        log('[OS] Continue using the same program..')
        return

    if prog_start_time is not None:
        log('>> program lifetime = %fs' %
            (time.time() - prog_start_time))  # or .clock(), cpu time
        log('-*- ' * 5)
    if cur_process:
        cur_process.terminate()  # or .kill()

    try:
        log('[OS] Switching program.. XD')
        prog_path = os.path.join(PROG_BASE, prog)
        cur_process = subprocess32.Popen(
            ['python', prog_path], stdout=None)  # None or open(LOG, 'a')
        prog_start_time = time.time()
        cur_program = prog
    except OSError, e:
        print e
        log('[OS] Program init error, rolling back.. X(')
        try:
            cur_process = subprocess32.Popen(
                ['python', cur_program], stdout=None)
        except OSError, e:
            print e


def download_program(url, prog):
    program_path = os.path.join(PROG_BASE, prog)
    if os.path.isfile(program_path):
        log('[HTTP] Use cached program :D')
    else:
        r = requests.get(url)
        with open(program_path, 'wb+') as prog:
            prog.write(r.content)
        log('[HTTP] Program downloaded :)')


def log(msg):
    print msg
    pub.publish(msg)


def client():
    global pub

    rospy.init_node('botrc_client', anonymous=True)
    pub = rospy.Publisher('botrc_client_dbg', String, queue_size=10)
    rate = rospy.Rate(1)    # 1Hz

    while not rospy.is_shutdown():
        rate.sleep()
        if random.random() < DOWN_RATE or cur_program is None:
            log('[Client] Simulates an algorithm sickness, turn for service...')
            device_dump = DeviceDumpRequest(2333)
            rospy.wait_for_service('botrc_consult')
            try:
                rtc_server = rospy.ServiceProxy('botrc_consult', DeviceDump)
                resp = rtc_server(device_dump)
                log("[Server] Resp %s: <%s>" % (resp.program, resp.url))

                download_program(resp.url, resp.program)
                switch_program(resp.program)
            except rospy.ServiceException, e:
                print e


if __name__ == '__main__':
    client()
