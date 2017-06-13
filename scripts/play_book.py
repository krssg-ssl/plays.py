import sys
sys.path.insert(0,'./../')

from plays.p_setposition import set_position

class PlayBook():
	"""
		Class to track the list of `plays`
	"""
	def __init__(self):
		self.play_id = dict()
		self.play_id['set_position'] = set_position