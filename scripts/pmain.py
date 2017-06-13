#!/usr/bin/env python

import rospy

from pSelect import pSelect
from role_node import role_node
from play_book import PlayBook

from krssg_ssl_msgs.msg import TacticPacket
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands

class Callback():
	def __init__(self, publisher):
		self.current_play  = None
		self.play_name     = None
		self.publisher     = publisher
		self.role_instance = role_node()
		self.pbook         = PlayBook()
		self.play_selector = pSelect()


	def retrieve(self, data):

		# update the belief state
		self.role_instance.bs_callback(data)

		if self.current_play == None:
			print 'Selecting new play'
			self.play_name    = self.play_selector.selectPlay(data)

			if self.play_name not in self.pbook.play_id:
				raise ValueError("There is no play named: {}".format(self.play_name))
			self.current_play = self.pbook.play_id[self.play_name]()

		# Execute the tactics of the play
	
rospy.init_node('play_py_node', anonymous=True)
pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)

callback = Callback(pub)
rospy.Subscriber('/belief_state', BeliefState, callback.retrieve)
rospy.spin()
