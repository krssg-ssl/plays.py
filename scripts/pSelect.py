import rospy

def refCallback(data):
	global refStatus
	refStatus = data

def selectPlay(self,data):
	
	if refStatus :  # TO DO To check whether need to use ref plays
		return refStatus
	else :
		return None  # TO DO To write select play and return it instead of none 

if __name__=='__main__':
	rospy.init_node('ref_play_node', anonymous=True)
	rospy.Subscriber('/ref_state', BeliefState, refCallback)
