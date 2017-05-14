#!/usr/bin/env python
import threading
import rospy
import pSelect
from krssg_ssl_msgs.msg import TacticPacket
from krssg_ssl_msgs.msg import BeliefState

thread_running = [False,False,False,False,False,False] # Global variable to check whichever threads are currently running

class botThread (threading.Thread):
	def __init__(self,botID,name, tacticID):
		threading.Thread.__init__(self)
		self.name = name
		self.botID = botID
		self.tacticID = tacticID
		# need to check for threadID

	def run(self):
		pass # depending on tactic ID need to call the tactic and tactic needs on completion needs to execute threadName.exit()
			# so threadName needs to be passed to tactic
			# we can also modify the role node to pass state and bot param and get tactic returned

state = BeliefState()

def Callback(data):
	rospy.loginfo('Received frame: {}'.format(data.frame_number))
	play_name = pSelect.selectPlay(data)
	if play_name : # TO DO check if refree play then use a refree play
		pass
	else :
		pass # TO DO the completed threads needs to be assigned a tactic and run using botThread object

if __name__=='__main__':
	rospy.init_node('play_py_node', anonymous=True)
	rospy.Subscriber('/belief_state', BeliefState, Callback)
	rospy.spin()
