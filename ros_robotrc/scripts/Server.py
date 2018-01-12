#!/usr/bin/env python

import random
import rospy
from ros_rt_control.srv import *
from std_msgs.msg import String

CHANGE_RATE = 0.5
srv = None
pub = None

def algorithm_select(req):
    log('Simulates an algorithm discovery..')
    program = random.random() < CHANGE_RATE and 'Add.py' or 'Mul.py'
    url = 'http://lab.kahsolt.tk/ros/%s' % program
    log('responding with %s: <%s>...' % (program, url))
    return DeviceDumpResponse(program, url)


def log(msg):
    print msg
    pub.publish(msg)


def server():
    global srv, pub

    rospy.init_node('botrc_server')
    srv = rospy.Service('botrc_consult', DeviceDump, algorithm_select)
    pub = rospy.Publisher('botrc_server_dbg', String, queue_size=10)
    log('Server init OK!')

    rospy.spin()


if __name__ == "__main__":
    server()
