#!/usr/bin/env python

import sys
import rospy
import threading
from plays_py.srv import role_to_play
from krssg_ssl_msgs.msg import BeliefState
from utils import tactics_union

# import tactic factory
sys.path.insert(0, './../../tactics_py/scripts')

import tactic_factory


class role_node(object):

	"""
	client node to communicate with play selector
	"""

	def __init__(self):
		print 'Waiting for the server node...'
		rospy.wait_for_service('node_role_com')
		self.state = BeliefState() 
		self.detected = 6
		self.begin = True

		# Assert if the tactic is completed and a new instance is to be created
		self.Tactic_0 = False
		self.Tactic_1 = False
		self.Tactic_2 = False
		self.Tactic_3 = False
		self.Tactic_4 = False
		self.Tactic_5 = False

		# Generate the role list
		self.role_list = [['' for i in range(2)] for j in range(self.detected)]


	def tactic_instance(self, bot_id, tactic_id, params):
		"""
			bot_id    : bot id
			tactic_id : enumeration of tactic
			params    : corresponding 'tactic_id' parameters
		"""
		# TODO : Update this list as and when new tactics are added

		if tactic_id == "TPosition":
			instance = tactic_factory.TPosition.TPosition(bot_id, self.state, params)
		elif tactic_id == "TStop":
			instance = tactic_factory.TStop.TStop(bot_id, self.state, params)
		else:
			instance = None

		return instance


	def update_rolelist(self, bot_id, play_id, referee=0):
		"""
			Updates the role of the 'bot_id' using learning algorithms

			@params	
			bot_id  : == -1 -> update the roles of all the bots
						 update the role list of bot_id	
			play_id : tactic to be choosen from this play_id
			referee : 0   -> normal play is run
						 else -> referee play will be run 									
		"""
		pass


	def update_execute(self, tactic):

		"""
			Method which updates and executes each bot's commands
		"""

		# Update the parameters of the current running tactics
		tactic.updateParams(self.state)

		# Check if the tactics are complete and choose new tactics
		if tactic.isComplete(self.state):
			bot_id = int(threading.currentThread().getName().split('_')[1])
			  
			self.play_id = self.client(bot_id)

			if self.play_id < 0:
				"""
					If the returned 'play_id' is < 0 => the play is of high priority and
					is from the referee and we need to update the roles of all the bots
				"""
				self.update_rolelist(0, 0, self.play_id)
			else:
				"""
					Update only the role list corresponding to 'bot_id'
				"""
				self.update_rolelist(bot_id, self.play_id)

			# 'tactic' is done, change the flag for this tactic
			if bot_id == 0:
				self.Tactic_0 = True
			if bot_id == 1:
				self.Tactic_1 = True
			if bot_id == 2:
				self.Tactic_2 = True
			if bot_id == 3:
				self.Tactic_3 = True
			if bot_id == 4:
				self.Tactic_4 = True
			if bot_id == 5:
				self.Tactic_5 = True

		else:
			tactic.execute(self.state)


	def bs_callback(self, data):

		"""
		update the belief belief_state
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

		# Begin all the threads for the first time, this is true only at 't=0'
		if self.begin:
			self.begin = False

			# TODO : Update the role list here
			self.update_rolelist(-1, 0)

			tac_0 = self.tactic_instance(0, self.role_list[0][0], self.role_list[0][1])		
			tac_1 = self.tactic_instance(1, self.role_list[1][0], self.role_list[1][1])		
			tac_2 = self.tactic_instance(2, self.role_list[2][0], self.role_list[2][1])		
			tac_3 = self.tactic_instance(3, self.role_list[3][0], self.role_list[3][1])		
			tac_4 = self.tactic_instance(4, self.role_list[4][0], self.role_list[4][1])		
			tac_5 = self.tactic_instance(5, self.role_list[5][0], self.role_list[5][1])		


			self.tactic_0 = threading.Thread(name="robot_0", target=self.update_execute, args=(tac_0))
			self.tactic_1 = threading.Thread(name="robot_1", target=self.update_execute, args=(tac_1))
			self.tactic_2 = threading.Thread(name="robot_2", target=self.update_execute, args=(tac_2))
			self.tactic_3 = threading.Thread(name="robot_3", target=self.update_execute, args=(tac_3))
			self.tactic_4 = threading.Thread(name="robot_4", target=self.update_execute, args=(tac_4))
			self.tactic_5 = threading.Thread(name="robot_5", target=self.update_execute, args=(tac_5))


		# Check if tactic is completed and update the instance accordingly
		if self.Tactic_0:
			self.Tactic_0 = False
			tac_0 = self.tactic_instance(0, self.role_list[0][0], self.role_list[0][1])		
			self.tactic_0 = threading.Thread(name="robot_0", target=self.update_execute, args=(tac_0))

		if self.Tactic_1:
			self.Tactic_1 = False
			tac_1 = self.tactic_instance(1, self.role_list[1][0], self.role_list[1][1])		
			self.tactic_1 = threading.Thread(name="robot_1", target=self.update_execute, args=(tac_1))

		if self.Tactic_2:
			self.Tactic_2 = False
			tac_2 = self.tactic_instance(2, self.role_list[2][0], self.role_list[2][1])		
			self.tactic_2 = threading.Thread(name="robot_2", target=self.update_execute, args=(tac_2))

		if self.Tactic_3:
			self.Tactic_3 = False
			tac_3 = self.tactic_instance(3, self.role_list[3][0], self.role_list[3][1])		
			self.tactic_3 = threading.Thread(name="robot_3", target=self.update_execute, args=(tac_3))

		if self.Tactic_4:
			self.Tactic_4 = False
			tac_4 = self.tactic_instance(4, self.role_list[4][0], self.role_list[4][1])		
			self.tactic_4 = threading.Thread(name="robot_4", target=self.update_execute, args=(tac_4))

		if self.Tactic_5:
			self.Tactic_5 = False
			tac_5 = self.tactic_instance(5, self.role_list[5][0], self.role_list[5][1])		
			self.tactic_5 = threading.Thread(name="robot_5", target=self.update_execute, args=(tac_5))

		# Start the threads
		self.tactic_0.start()
		self.tactic_1.start()
		self.tactic_2.start()
		self.tactic_3.start()
		self.tactic_4.start()
		self.tactic_5.start()


	def node(self):
		print 'Found {} server'.format('node_role_com')
		self.client = rospy.ServiceProxy('node_role_com', role_to_play)
		rospy.Subscriber('/belief_state', BeliefState, self.bs_callback)
		rospy.spin()
