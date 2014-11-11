from data import *
from schedule import *
from Interval import *
from time import time
from collections import *
from matplotlib.pyplot import *

dates = []
for i in xrange(1, 32):
	day = str(i)
	if i < 10:
		day = '0' + day
	dates.append('2014-01-' + day)

folder = '../graph/'
min_flights = 100

def q2b():
	print 'Q2B'
	print 'How many gates are needed?'
	print 'Is there any relationship between the number of flights and the number of gates needed?'
	flights_to_gates = []
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			intervals = [Interval(flight_info) for flight_info in flight_infos]
			gates = assign(intervals)
			flights_to_gates.append((len(intervals), len(gates)))

	# with open(folder + '2b.dat', 'w') as f:
	# 	f.write('# Number of flights\tNumber of gates needed\n')
	# 	print '# Number of flights', '\t', 'Number of gates needed'
	# 	for flights, gates in flights_to_gates:
	# 		print flights, '\t', gates
	# 		f.write('{}\t{}\n'.format(flights, gates))
	xs = 'Number of flights'
	ys = 'Number of gates needed'
	xlabel(xs)
	ylabel(ys)
	scatter(*zip(*flights_to_gates))
	axis('tight')
	savefig(folder + '2b.png', bbox_inches='tight')
	cla()

def q3a():
	print 'Q3A'
	print 'How much random delay is needed before we see a collision?'
	slack_to_delays = []
	p = 0.948 # avg probability to be delayed from our data
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			for i in xrange(0, 1000):
				delay_flight_infos(flight_infos, p, -i, i)
				delayed_intervals = [Interval(flight_info) for flight_info in flight_infos]
				gates = assign(delayed_intervals)
				slack = min([min(gate.slacks()) for gate in gates])
				num_collisions = sum([gate.collisions() for gate in gates])
				if num_collisions > 0:
					break
			try:
				assert slack <= 2*i
			except:
				print 'error', slack, i
			slack_to_delays.append((slack, i))

	# with open(folder + '3ai.dat', 'w') as f:
	# 	f.write('# Slack (mins)\tMagnitude of delay (mins)\n')
	# 	print '# Slack (mins)\tMagnitude of delay (mins)'
	# 	for slack, delays in slack_to_delays:
	# 		print slack, '\t', delays
	# 		f.write('{}\t{}\n'.format(slack, delays))
	xs = 'Slack (mins)'
	ys = 'Magnitude of random delay (mins)'
	xlabel(xs)
	ylabel(ys)
	scatter(*zip(*slack_to_delays))
	axis('tight')
	xlim(-1, 16)
	savefig(folder + '3ai.png', bbox_inches='tight')
	cla()
	quit()

	print 'For a given level of random delay, how many gate collisions do we see?'
	slack_to_collisions = []
	delay = 24 # average delay from our data
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			delay_flight_infos(flight_infos, 0.95, -delay, delay)
			delayed_intervals = [Interval(flight_info) for flight_info in flight_infos]
			gates = assign(delayed_intervals)
			slack = min([min(gate.slacks()) for gate in gates])
			if slack > 50:
				continue
			num_collisions = sum([gate.collisions() for gate in gates])
			slack_to_collisions.append((slack, num_collisions))

	# with open(folder + '3aii.dat', 'w') as f:
	# 	header = '# Slack (mins)\tNumber of gate collisions'
	# 	print header
	# 	f.write(header + '\n')
	# 	for slack, collisions in slack_to_collisions:
	# 		print slack, '\t', collisions
	# 		f.write('{}\t{}\n'.format(slack, collisions))
	xs = 'Slack (mins)'
	ys = 'Number of gate collisions'
	xlabel(xs)
	ylabel(ys)
	scatter(*zip(*slack_to_collisions))
	axis('tight')
	savefig(folder + '3aii.png', bbox_inches='tight')
	cla()

	print 'Now, use the actual delays from the real dataset. How many gate collisions do we see?'
	delays_to_collisions = []
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			gates = assign(intervals(flight_infos))
			num_collisions = sum([gate.collisions() for gate in gates])
			delays_to_collisions.append((avg_delay(flight_infos), num_collisions))

	# with open(folder + '3aiii.dat', 'w') as f:
	# 	print '# Magnitude of mean delay (mins)\tNumber of gate collisions'
	# 	f.write('# Magnitude of mean delay (mins)\tNumber of gate collisions\n')
	# 	for delays, collisions in delays_to_collisions:
	# 		print delays, '\t', collisions
	# 		f.write('{}\t{}\n'.format(delays, collisions))
	xs = 'Magnitude of mean delay (mins)'
	ys = 'Number of gate collisions'
	xlabel(xs)
	ylabel(ys)
	scatter(*zip(*delays_to_collisions))
	axis('tight')
	savefig(folder + '3aiii.png', bbox_inches='tight')
	cla()

def q3b():
	print 'Q3B'
	delays_to_reassignment_optimal_gates = []
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			intervals = [Interval(flight_info) for flight_info in flight_infos]
			gates = assign(intervals)
			optimal_gates = assign(intervals, 0, delayed_start_time, delayed_end_time)
			reassignment = reassign(gates, intervals)
			delays_to_reassignment_optimal_gates.append((avg_delay(flight_infos), (reassignment, optimal_gates)))

	print 'For the delays in the dataset, how many gates do we need?'
	# with open(folder + '3bi.dat', 'w') as f:
	# 	header = '# Magnitude of mean delay (mins)\tNumber of gates\tNumber of optimal gates\tDifference'
	# 	print header
	# 	f.write(header + '\n')
	# 	for delays, reassignment_optimal_gates in delays_to_reassignment_optimal_gates:
	# 		reassignment = reassignment_optimal_gates[0]
	# 		len_gates = len(reassignment[0]) + len(reassignment[1])
	# 		len_optimal_gates = len(reassignment_optimal_gates[1])
	# 		difference = len_gates - len_optimal_gates
	# 		print delays, '\t', len_gates, '\t', len_optimal_gates, '\t', difference
	# 		f.write('{}\t{}\t{}\t{}\n'.format(delays, len_gates, len_optimal_gates, difference))
	xs = 'Magnitude of mean delay (mins)'
	ys = 'Number of gates'
	xlabel(xs)
	ylabel(ys)
	x = []
	y1 = []
	y2 = []
	y3 = []
	for delays, reassignment_optimal_gates in delays_to_reassignment_optimal_gates:
		reassignment = reassignment_optimal_gates[0]
		len_gates = len(reassignment[0]) + len(reassignment[1])
		len_optimal_gates = len(reassignment_optimal_gates[1])
		difference = len_gates - len_optimal_gates
		x.append(delays)
		y1.append(len_gates)
		y2.append(len_optimal_gates)
		y3.append(difference)
	scatter(x, y1, color='green', label='Our algorithm')
	scatter(x, y2, color='blue', label='Optimal')
	scatter(x, y3, color='red', label='Difference')
	legend()
	axis('tight')
	savefig(folder + '3bi.png', bbox_inches='tight')
	cla()

	print 'How does the number of extra gates needed scale with the delays?'
	# with open(folder + '3bii.dat', 'w') as f:
	# 	header = '# Magnitude of mean delay (mins)\tNumber of extra gates\tNumber of optimal extra gates\tDifference'
	# 	print header
	# 	f.write(header + '\n')
	# 	for delays, reassignment_optimal_gates in delays_to_reassignment_optimal_gates:
	# 		reassignment = reassignment_optimal_gates[0]
	# 		len_extra_gates = len(reassignment[1])
	# 		len_optimal_extra_gates = len(reassignment_optimal_gates[1]) - len(reassignment[0])
	# 		difference = len_extra_gates - len_optimal_extra_gates
	# 		print delays, '\t', len_extra_gates, '\t', len_optimal_extra_gates, '\t', difference
	# 		f.write('{}\t{}\t{}\t{}\n'.format(delays, len_extra_gates, len_optimal_extra_gates, difference))
	xs = 'Magnitude of mean delay (mins)'
	ys = 'Number of extra gates'
	xlabel(xs)
	ylabel(ys)
	x = []
	y1 = []
	y2 = []
	y3 = []
	for delays, reassignment_optimal_gates in delays_to_reassignment_optimal_gates:
		reassignment = reassignment_optimal_gates[0]
		len_extra_gates = len(reassignment[1])
		len_optimal_extra_gates = len(reassignment_optimal_gates[1]) - len(reassignment[0])
		difference = len_extra_gates - len_optimal_extra_gates
		x.append(delays)
		y1.append(len_extra_gates)
		y2.append(len_optimal_extra_gates)
		y3.append(difference)
	scatter(x, y1, color='green', label='Our algorithm')
	scatter(x, y2, color='blue', label='Optimal')
	scatter(x, y3, color='red', label='Difference')
	legend()
	axis('tight')
	savefig(folder + '3bii.png', bbox_inches='tight')
	cla()

def q4():
	print 'Q4'
	extra_gates_to_reassignment = []
	for date in dates:
		print date
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date, min_flights)
		for airport, flight_infos in airport_to_flight_infos.items():
			intervals = [Interval(flight_info) for flight_info in flight_infos]
			original_gates = assign(intervals)
			for i in xrange(0, 101):
				num_extra_gates = int((float(i)/100) * len(intervals))
				gates = assign(intervals, len(original_gates) + num_extra_gates)
				reassignment = reassign(gates, intervals)
				# [number of gates, number of overflow gates, number of reassignments]
				reassignment = [len(reassignment[0]), len(reassignment[1]), reassignment[2]]
				extra_gates_to_reassignment.append((i, reassignment))
		
	print 'Show, via experiment, that this minimizes the number of gate reassignments.'
	# with open(folder + '4i.dat', 'w') as f:
	# 	header = '# Percentage of extra gates\tNumber of reassignment\tNumber of overflow gates'
	# 	f.write(header + '\n')
	# 	# print header
	# 	for extra_gates, reassignment in extra_gates_to_reassignment:
	# 		# print extra_gates, '\t', reassignment[2], '\t', len(reassignment[1])
	# 		f.write('{}\t{}\t{}\n'.format(extra_gates, reassignment[2], reassignment[1]))
	# xs = 'Percentage of extra gates'
	# ys = 'Number of reassignment'
	# xlabel(xs)
	# ylabel(ys)
	# x = []
	# y = []
	# for extra_gates, reassignment in extra_gates_to_reassignment:
	# 	x.append(extra_gates)
	# 	y.append(reassignment[2])
	# scatter(x, y)
	# axis('tight')
	# savefig(folder + '4i.png', bbox_inches='tight')
	# cla()

	print 'Prove that your assignment can handle a certain level of delay.'
	# with open(folder + '4ii.dat', 'w') as f:
	# 	header = '# Percentage of extra gates\tPercentage of success'
	# 	f.write(header + '\n')
	# 	# print header
	# 	extra_gates_to_num_success = defaultdict(int)
	# 	extra_gates_to_num_total = defaultdict(int)
	# 	for extra_gates, reassignment in extra_gates_to_reassignment:
	# 		if reassignment[1] == 0:
	# 			extra_gates_to_num_success[extra_gates] += 1
	# 		extra_gates_to_num_total[extra_gates] += 1
	# 	for extra_gates, num_success in extra_gates_to_num_success.items():
	# 		percentage_success = float(num_success)/extra_gates_to_num_total[extra_gates]
	# 		# print extra_gates, '\t', percentage_success
	# 		f.write('{}\t{}\n'.format(extra_gates, percentage_success))
	xs = 'Percentage of extra gates'
	ys = 'Percentage of success'
	xlabel(xs)
	ylabel(ys)
	x = []
	y = []
	extra_gates_to_num_success = defaultdict(int)
	extra_gates_to_num_total = defaultdict(int)
	for extra_gates, reassignment in extra_gates_to_reassignment:
		if reassignment[1] == 0:
			extra_gates_to_num_success[extra_gates] += 1
		extra_gates_to_num_total[extra_gates] += 1
	for extra_gates, num_success in extra_gates_to_num_success.items():
		percentage_success = float(num_success)/extra_gates_to_num_total[extra_gates]
		x.append(extra_gates)
		y.append(percentage_success)
	scatter(x, y)
	axis('tight')
	ylim(-0.05, 1.05)
	savefig(folder + '4ii.png', bbox_inches='tight')
	cla()

# q2b()
q3a()
# q3b()
# q4()