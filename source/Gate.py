class Gate:
	def __init__(self, interval=None):
		self.intervals = [] if interval is None else [interval]

	def __repr__(self):
		return str(self.intervals)

	def __getitem__(self, key):
		return self.intervals[key]

	def __len__(self):
		return len(self.intervals)

	def index(self, interval):
		return self.intervals.index(interval)

	def append(self, interval):
		self.intervals.append(interval)

	def insert(self, i, interval):
		self.intervals.insert(i, interval)

	def remove(self, interval):
		return self.intervals.remove(interval)

	# returns a list of slacks where slack is the difference between two intervals
	# in the case the gate has only one interval, then the slack is inf
	def slacks(self):
		slacks = []
		if len(self.intervals) == 1:
			slacks.append(float('inf'))
		else:
			for i in xrange(0, len(self.intervals)-1):
				slacks.append(self.intervals[i+1].scheduled_start_time - self.intervals[i].scheduled_end_time)
		return slacks

	# returns the number of collisions in this gate
	def collisions(self):
		num_collisions = 0
		for interval1 in self.intervals:
			for interval2 in self.intervals:
				if interval1 is interval2:
					continue
				if interval1.delayed_start_time < interval2.delayed_start_time: # haven seen interval 2 yet
					if interval1.delayed_end_time > interval2.scheduled_start_time:
						num_collisions += 1
				else:
					if interval2.delayed_end_time > interval1.delayed_start_time:
						num_collisions += 1
		return num_collisions

	# returns the index to a free slot for interval
	def free_index(self, interval):
		i = 0
		while i < len(self.intervals) and interval.delayed_end_time > self.intervals[i].delayed_start_time:
			i += 1
		if i == 0 or self.intervals[i-1].delayed_end_time <= interval.delayed_start_time:
			return i
		else:
			return -1