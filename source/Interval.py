class Interval:
	def __init__(self, flight_info):
		self.index = flight_info.index
		self.scheduled_start_time = flight_info.scheduled_time
		if flight_info.is_depart:
			self.scheduled_start_time -= 90
			self.scheduled_end_time = flight_info.scheduled_time + 30

			if flight_info.scheduled_time < flight_info.actual_time:
				self.delayed_start_time = self.scheduled_start_time
				self.delayed_end_time = flight_info.actual_time + 10
				self.delayed_end_time = max(self.delayed_end_time, self.scheduled_end_time)
			elif flight_info.scheduled_time == flight_info.actual_time:
				self.delayed_start_time = self.scheduled_start_time
				self.delayed_end_time = self.scheduled_end_time
			elif flight_info.scheduled_time > flight_info.actual_time:
				self.delayed_start_time = flight_info.actual_time - 90
				self.delayed_end_time = flight_info.actual_time + 10
		else:
			self.scheduled_end_time = flight_info.scheduled_time + 45
			self.delayed_start_time = flight_info.actual_time
			self.delayed_end_time = flight_info.actual_time + 45

	def __repr__(self):
		return str((self.index, self.scheduled_start_time, self.scheduled_end_time, self.delayed_start_time, self.delayed_end_time))

	def delayed(self):
		return self.scheduled_start_time != self.delayed_start_time or self.scheduled_end_time != self.delayed_end_time

def scheduled_start_time(interval):
	return interval.scheduled_start_time

def scheduled_end_time(interval):
	return interval.scheduled_end_time

def delayed_start_time(interval):
	return interval.delayed_start_time

def delayed_end_time(interval):
	return interval.delayed_end_time
