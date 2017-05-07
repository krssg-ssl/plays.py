from ctypes import *

"""
-> define one separate class for each of the tactics parameters
   as given in 'tactics/tactics.h'
-> finally create an union of all the above classes
"""

# TODO : Complete the remaining tactic parameters from 'tactics/tactics.h' file

class GoalieP(Structure):
	_fields_ = []

class ClearP(Structure):
	_fields_ = []

class BlockP(Structure):
	_fields_ = [("dist", c_float), 
					("side", c_int)]

class DefendLineP(Structure):
	_fields_ = [("x1", c_int), 
					("y1", c_int), 
					("x2", c_int), 
					("y2", c_int),
					("radius", c_int)]


"""
Create union of all the above classes
"""
class Param(Union):
	_fields_ = [("GoalieP", GoalieP), 
					("ClearP", ClearP), 
					("BlockP", BlockP), 
					("DefendLineP", DefendLineP)]
