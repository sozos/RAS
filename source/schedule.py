from FlightInfo import FlightInfo
from Interval import *
from Gate import Gate
from Queue import *
from random import *

def assign(intervals, num_gates=0, start_time=scheduled_start_time, end_time=scheduled_end_time):
	gates = [Gate() for i in xrange(0, num_gates)]

	# initialise priority queue
	pq = PriorityQueue()
	for gate in gates:
		pq.put((-9999, gate))

	sorted_intervals = sorted(intervals, key=start_time)
	while sorted_intervals:
	 	interval = sorted_intervals.pop(0);
		if not pq.empty():
			end_time_gate = pq.get()
			earliest_end_time = end_time_gate[0]
			gate = end_time_gate[1]
			if earliest_end_time <= start_time(interval):
				gate.append(interval)
				pq.put((end_time(interval), gate))
				continue
			pq.put(end_time_gate)
		pq.put((end_time(interval), Gate(interval)))

	gates = []
	while not pq.empty():
		gates.append(pq.get()[1])
	return gates

# delays flights with probability p by a number in [min_delay, max_delay] in minutes
def delay_flight_infos(flight_infos, p, min_delay, max_delay):
	for flight_info in flight_infos:
		if random() < p:
			dx = randint(min_delay, max_delay)
			flight_info.add_delay(dx)
		else:
			flight_info.add_delay(0)

# reassigns intervals in gates if there are collisions
# returns [gates, overflow gates, # of reassignments]
def reassign(gates, intervals):
	def get_slack(gate, index, interval):
		start = gate[index+1].scheduled_start_time if index < len(gate)-1 else 1439
		return start - interval.delayed_end_time

	interval_to_gate = {}
	for gate in gates:
		for i, interval in enumerate(gate):
			interval_to_gate[interval] = gate

	reassign_count = 0
	overflow_gates = []
	sorted_intervals = sorted(intervals, key=delayed_start_time)
	while sorted_intervals:
		interval = sorted_intervals.pop(0)
		if interval.delayed():
			gate = interval_to_gate[interval]
			index = gate.index(interval)
			
			# check for collisions, maybe no need to reassign
			collision = ((index > 0 and not gate[index-1].delayed_end_time <= interval.delayed_start_time)
				or
				(index+1 < len(gate) and not interval.delayed_end_time <= gate[index+1].scheduled_start_time))

			if not collision:
				continue

			# find gate with most slack to reassign to
			gate.remove(interval)
			most_slack_gate = None
			most_slack_index = None
			most_slack = None
			for gate2 in gates + overflow_gates:
				index = gate2.free_index(interval)
				if index < 0: # no free slots
					continue
				slack = get_slack(gate2, index, interval)
				if most_slack is None or most_slack < slack:
					most_slack_gate = gate2
					most_slack_index = index
					most_slack = slack
			if most_slack is None: # no gates are free
				overflow_gates.append(Gate(interval))
			else:
				most_slack_gate.insert(most_slack_index, interval)
			reassign_count += 1
	return [gates, overflow_gates, reassign_count]
