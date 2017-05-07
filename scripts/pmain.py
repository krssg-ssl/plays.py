#!/usr/bin/env python

import rospy
from krssg_ssl_msgs.msg import TacticPacket
from krssg_ssl_msgs.msg import BeliefState

state = BeliefState()
def Callback(data):
	rospy.loginfo('Received frame: {}'.format(data.frame_number))
	
	state.isteamyellow                 = data.isteamyellow
	state.frame_number                 = data.frame_number
	state.t_capture                    = data.t_capture
	state.t_sent                       = data.t_sent
	state.ballPos                      = data.ballPos
	state.ballVel                      = data.ballVel
	state.awayPos                      = data.awayPos
	state.homePos                      = data.homePos
	state.ballDetected                 = data.ballDetected
	state.homeDetected                 = data.homeDetected
	state.awayDetected                 = data.awayDetected
	state.our_goalie                   = data.our_goalie
	state.opp_goalie                   = data.opp_goalie
	state.our_bot_closest_to_ball      = data.our_bot_closest_to_ball
	state.opp_bot_closest_to_ball      = data.opp_bot_closest_to_ball
	state.opp_bot_marking_our_attacker = data.opp_bot_marking_our_attacker
	state.ball_at_corners              = data.ball_at_corners
	state.ball_in_our_half             = data.ball_in_our_half
	state.ball_in_our_possession       = data.ball_in_our_possession

	publishing()
	return

def publishing():
	tp0_pub = rospy.Publisher('tactic_0', TacticPacket, queue_size=1000)
	tp1_pub = rospy.Publisher('tactic_1', TacticPacket, queue_size=1000)
	tp2_pub = rospy.Publisher('tactic_2', TacticPacket, queue_size=1000)
	tp3_pub = rospy.Publisher('tactic_3', TacticPacket, queue_size=1000)
	tp4_pub = rospy.Publisher('tactic_4', TacticPacket, queue_size=1000)
	tp5_pub = rospy.Publisher('tactic_5', TacticPacket, queue_size=1000)

	tp0 = TacticPacket()
	tp1 = TacticPacket()
	tp2 = TacticPacket()
	tp3 = TacticPacket()
	tp4 = TacticPacket()
	tp5 = TacticPacket()


	tp0_pub.publish(tp0)
	tp1_pub.publish(tp1)
	tp2_pub.publish(tp2)
	tp3_pub.publish(tp3)
	tp4_pub.publish(tp4)
	tp5_pub.publish(tp5)


rospy.init_node('play_py_node', anonymous=True)
rospy.Subscriber('/belief_state', BeliefState, Callback)
rospy.spin()
