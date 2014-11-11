import math

class FlightInfo:
	def __init__(self, index, is_depart, scheduled_time, actual_time):
		self.index = index
		self.is_depart = is_depart
		self.scheduled_time = scheduled_time
		self.actual_time = actual_time

	def __repr__(self):
		return str((self.index, self.is_depart, self.scheduled_time, self.actual_time))

	def delay(self):
		return int(math.fabs(self.actual_time - self.scheduled_time))

	# delays the interval by dx where dx is the change in minutes
	def add_delay(self, dx):
		self.actual_time = self.scheduled_time + dx

	# returns true if the flight is delayed, else false
	def delayed(self):
		return self.scheduled_time != self.actual_time