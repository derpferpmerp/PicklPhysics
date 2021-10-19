import math
import numpy as np
import scipy
import matplotlib.pyplot as plt
import random
import json
import re

def printJson(data:dict):
	'''
	Function: printJson
	Summary: Beautifies and Prints Json to System Output
	Examples: printJson({ "a":"b", "c":4 })
	Attributes: 
		@param (data:dict): The Json to Beautify
	Returns: Nothing
	'''
	# Determine Validity of Input Arguments
	if not isinstance(data, dict):
		incType = str(type(data))
		formattedType = re.search("(?<=\\<class \\\')(.*?)(?=\\\'\\>)", incType).group()
		raise TypeError(f"Incorrect Input type for \"data\": \"{formattedType}\"")
	
	print(json.dumps(data, indent=4))
	print("")

def safeRoot(number):
	'''
	Function: safeRoot
	Summary: Calculates the Square Root of the Number, but extracts the Negative
	Examples:
	(1) safeRoot(-1) -> -sqrt(1) -> -1
	(2) safeRoot(-64) -> -8
	(3) safeRoot(64) -> 8
	Attributes: 
		@param (number): The Number to Square Root
	Returns: float
	'''
	if number == 0:
		root = 0
	else:
		root = (number/abs(number))
		root *= math.sqrt(abs(number))
	return root

class AbstractNumber(object):
	"""docstring for AbstractNumber"""
	def __init__(self, num):
		super(AbstractNumber, self).__init__()
		self.number = num

	def cot(self):
		return 1/math.tan(self.number)

	def csc(self):
		return 1/math.sin(self.number)

	def sec(self):
		return 1/math.cos(self.number)
		
def allInList(items:list, lst:list):
	'''
	Function: allInList
	Summary: Checks if All Items are in the List
	Examples:
	(1) allInList([1,2,3,4],[2,3,4]) -> False
	(2) allInList([1,2,3,4],[75,3,22,1,25,2,6,4]) -> True
	Attributes: 
		@param (items:list): List of Items to Iterate Through
		@param (lst:list): The List to Check From
	Returns: Boolean
	'''
	for x in items:
		if x not in lst:
			return False
	return True

class CircularObject(object):
	"""docstring for CircularObject"""
	def __init__(self, **kwargs):
		'''
		Function: __init__
		Summary: Initialize Variables
		Attributes: 
			@param (MASS): The Object's Mass
			@param (GRAV): The Object's Gravitational Acceleration
			@param (VEL0): The Object's Initial Velocity
			@param (RADIUS): The Object's Radius
			@param (DIMENSIONS): The Object's Dimensional Constant ( 2 : CircularObject | 3 : Sphere )
		Returns: NA
		'''
		
		super(CircularObject, self).__init__()
		presets = dict(
			MASS=100,
			GRAV=9.81,
			VEL0=1,
			RADIUS=1,
			DIMENSIONS=2
		)
		allowed_keys = set(list(presets.keys()))
		self.__dict__.update((key, presets[key]) for key in allowed_keys)
		self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)

		self.momentOfInertia()

	def showCurrentData(self):
		printJson(dict(vars(self)))

	def momentOfInertia(self):
		if self.DIMENSIONS == 2:
			self.MOI = (4/3)
			self.RMOI = (3/4)
		elif self.DIMENSIONS == 3:
			self.MOI = (10/7)
			self.RMOI = (7/2)

	def InclinedPlane(self, v_i=False, h=False, g=False, theta=False, mu=False):
		'''
		Function: InclinedPlane
		Summary: Simulates the Physics Between the GameObject and the Slope
		Examples: InclinedPlane(v_i=10)
		Attributes: 
			@param (v_i): The Object's Initial Velocity
			@param (h) default=5: The Object's Initial Altitude
			@param (g) default=9.81: The Object's Gravitational Acceleration
			@param (theta) default=(pi/4): The Angle of the Slope of the Incline
			@param (mu) default=0.1: The Frictional Coefficient of the System
		Returns: dict
		'''

		self.momentOfInertia()

		if not v_i:
			print(f"[ WARN ] Initial Velocity (v_i) Not Supplied. Defaulting to {self.VEL0}")
			v_i = self.VEL0
		if not h:
			print(f"[ WARN ] Initial Height (h) Not Supplied. Defaulting to 5")
			h = 5
		if not g:
			print(f"[ WARN ] System Gravity (g) Not Supplied. Defaulting to {self.GRAV}")
			g = self.GRAV
		if not theta or (not isinstance(theta, float) and not isinstance(theta, int)):
			print(f"[ WARN ] Plane Angle (theta) Not Supplied or Invalid Type. Defaulting to \u03c0/4 ( 45\u00b0 )")
			theta = math.radians(45)
		if not mu:
			print(f"[ WARN ] Friction Coefficient \u00b5 (mu) Not Supplied. Defaulting to 0.1")
			mu = 0.1

		v_f = (v_i ** 2)
		v_f += self.MOI * (g * h) # (should be 4/3)
		v_f = safeRoot(v_f)
		
		a = (self.MOI * g * h * math.sin(theta)) - (v_i * v_i * math.sin(theta))
		a /= 2 * (h)

		thetaTrig = AbstractNumber(theta)

		a_wfric = a - (mu * g * thetaTrig.cot())

		finaldist = (v_f ** 2) - (v_i ** 2)
		finaldist /= (2 * a)

		maxDistance = h / math.sin(theta)
		percentDistance = round(100 * (finaldist / maxDistance))

		timepassed = (-1 * v_i) + safeRoot((2 * finaldist * a) + (v_i ** 2))
		timepassed /= a

		out = {
			"Acceleration": a,
			"Final Velocity": v_f,
			"Time Passed": timepassed
		}
		return out

	def Projectile(self, **kwargs):
		'''
		Function: Projectile
		Summary: Simulates Throwing the Object in the Air
		Examples:
		(1) instance.Projectile(theta=NUM,v=NUM)
		(2) instance.Projectile(vx=NUM,vy=NUM)"
		Attributes: 
			@param (theta) group=1: Launch Angle (Radians)
			@param (v) group=1: Launch Velocity (m/s)
			@param (vx) group=2: Horizontal Component of Launch Velocity
			@param (vy) group=2: Vertical Component of Launch Velocity
			@param (h) group=None: Initial Projectile Altitude
		Returns: dict
		'''
		
		h_i = 0
		kwargKeys = []
		kwargFixed = {}
		for k, v in list(kwargs.items()):
			lwr = k.lower()
			kwargKeys.append(lwr)
			kwargFixed[lwr] = v

		if "h" in kwargKeys:
			h_i = kwargFixed["h"]

		if allInList(["theta","v"], kwargKeys):
			theta = kwargFixed["theta"]
			v_i = kwargFixed["v"]
			vx, vy = [ v_i * math.cos(theta), v_i * math.sin(theta) ]
		elif allInList(["vx","vy"], kwargKeys):
			vx, vy = [kwargFixed["vx"], kwargFixed["vy"]]
			theta = math.atan(vy / vx)
			v_i = math.sqrt((vx ** 2) + (vy ** 2))
		else:
			print("")

			argsUsed = []
			for x in range(len(list(kwargs.items()))):
				k, v = list(kwargs.items())[x]
				argsUsed.append(f"( Index {x} ) {k} = {v}")
			argsUsed = "\n"+"\n".join(argsUsed)

			result = "\n".join([
				"You Must Run Projectile with Either Set of Arguments:",
				"(1) instance.Projectile(theta=NUM,v=NUM)",
				"(2) instance.Projectile(vx=NUM,vy=NUM)",
				f"You Ran with the Arguments: {argsUsed}\n"
			])
			raise TypeError(result)

		sin = math.sin(theta)
		cos = math.cos(theta)

		airtime = (v_i * sin) + math.sqrt(( (v_i ** 2) * (sin * sin) ) + (2 * self.GRAV * h_i))
		airtime /= self.GRAV

		maxRange = (v_i * cos) * airtime

		maxHeight = v_i * v_i * sin * sin
		maxHeight /= 2 * self.GRAV
		maxHeight += h_i

		peakTime = (v_i * math.sin(theta)) / self.GRAV

		impactVelocity = math.sqrt(2 * self.GRAV * maxHeight)

		print(
			"\n[ SETUP ]",
			f"Velocity: {v_i} < {round(vx,2)}, {round(vy,2)} >",
			f"Launch Angle (\u03B8): {round(theta,2)} rad ( {round(math.degrees(theta))}\u00b0 )",
			f"Height: {h_i}\n",
			"[ RESULTS ]",
			f"Air Time: {airtime}",
			f"Max Height: {maxHeight} ( At {round(peakTime,3)}s )",
			f"Horizontal Displacement: {maxRange}",
			f"Impact Velocity: {impactVelocity}",
			sep="\n"
		)

		return dict(
			t=airtime,
			hmax=maxHeight,
			xmax=maxRange
		)

	def Rolling(self, v=10, mu=0.1, g=False):
		'''
		Function: Rolling
		Summary: Simulates A Ball Rolling Until it Stops
		Examples: Rolling(v=4)
		Attributes: 
			@param (v) default=10: Initial Velocity of Object
			@param (mu) default=0.1: Friction Coefficient
			@param (g) default=9.81: System Gravity
		Returns: dict
		'''
		v_i = v
		self.momentOfInertia()
		if not g: g = self.GRAV

		stoppingDistance = self.RMOI * ((v_i * v_i) / (mu * g))
		timeToStop = (2 * self.RMOI * v_i) / (mu * g)

		print(
			"\n[ SETUP ]",
			f"Velocity: {v_i}",
			f"Friction Coefficient (\u00b5): {mu}",
			f"Gravity: {g}\n",
			"[ RESULTS ]",
			f"Stopping Distance: {stoppingDistance}",
			f"Stopping Time: {timeToStop}\n",
			sep="\n"
		)

		return dict(
			distance=stoppingDistance,
			t=timeToStop
		)




h = CircularObject(MASS=1)

r3 = h.InclinedPlane()
printJson(r3)
r = h.Projectile(
	theta=math.radians(15),
	v=20,
	h=10
)
printJson(r)
r2 = h.Rolling(v=4)
printJson(r2)