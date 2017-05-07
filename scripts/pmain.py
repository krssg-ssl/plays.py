#!/usr/bin/env python

import rospy
from krssg_ssl_msgs.msg import TacticPacket
from krssg_ssl_msgs.msg import BeliefState

state = BeliefState()
def Callback(data):
	rospy.loginfo('Received frame: {}'.format(data.frame_number))
	pexec = pExec()
	play_name = pexec.selectPlay(data)
	
rospy.init_node('play_py_node', anonymous=True)
rospy.Subscriber('/belief_state', BeliefState, Callback)
rospy.spin()
