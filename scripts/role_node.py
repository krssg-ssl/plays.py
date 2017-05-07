#!/usr/bin/env python

import rospy
from plays_py.srv import role_to_play
from krssg_ssl_msgs.msg import BeliefState
from utils import tactics_union
"""
client node to communicate with play selector
"""

class role_node(object):

	def __init__(self):
		rospy.wait_for_service('node_role_com')
		self.state = BeliefState() 
		self.detected = 6

		# Generate the role list
		self.role_list = [['' for i in range(2)] for j in range(self.detected)]

	def should_ping(self):
		"""
		TODO: Add the conditions here if we need to ping the server
		"""
		pass

	def bs_callback(self, data):

		"""
		update the belief state
		"""
		self.state.isteamyellow                 = data.isteamyellow
		self.state.frame_number                 = data.frame_number
		self.state.t_capture                    = data.t_capture
		self.state.ballPos                      = data.ballPos
		self.state.ballVel                      = data.ballVel
		self.state.awayPos                      = data.awayPos
		self.state.homePos                      = data.homePos
		self.state.awayVel                      = data.awayVel
		self.state.homeVel                      = data.homeVel
		self.state.ballDetected                 = data.ballDetected
		self.state.homeDetected                 = data.homeDetected
		self.state.awayDetected                 = data.awayDetected
		self.state.our_bot_closest_to_ball      = data.our_bot_closest_to_ball
		self.state.opp_bot_closest_to_ball      = data.opp_bot_closest_to_ball
		self.state.our_goalie                   = data.our_goalie
		self.state.opp_goalie                   = data.opp_goalie
		self.state.opp_bot_marking_our_attacker = data.opp_bot_marking_our_attacker
		self.state.ball_at_corners              = data.ball_at_corners
		self.state.ball_in_our_half             = data.ball_in_our_half
		self.state.ball_in_our_possession       = data.ball_in_our_possession

		self.detected = 0
		for idx in range(len(self.state.homeDetected)):
			if self.state.homeDetected[idx]==True:
				self.detected += 1

		"""
		Check if need to ping the server to update role list
		"""
		if self.should_ping():
			"""
			Returns play_id of the current play from play selector
			"""
			self.play_id = self.client(True)
		else:
			pass

		"""
		TODO: 
			#1 Call the tactics update parameters for the selected tactics
			#2 Call the tactics execution functions for all the roles here
		"""


	def node(self):
		print 'Found {} server'.format('node_role_com')
		self.client = rospy.ServiceProxy('node_role_com', role_to_play)
		rospy.Subscriber('/belief_state', BeliefState, self.bs_callback)
		rospy.spin()

role = role_node()
role.node()
