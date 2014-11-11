from FlightInfo import *
from Interval import *

# Converts time from 24h format to minutes in the range [0,1439]
def time_to_minutes(time_string):
	t = int(time_string)
	t_hr = t / 100
	t_min = t % 100
	return t_hr * 60 + t_min

# Add duration to time t
def add_time(t, duration):
	return t + duration

# Returns the time difference in minutes, time2 must be equal or later to time1
def time_diff(time1, time2):
	return int(math.fabs(time2 - time1))

# prints the avg probablility p of being delayed, and the avg delays defined by |depart - actual|
def get_stats():
	total_delay = 0
	total_p = 0
	total_flights = 0
	for date in dates:
		airport_to_flight_infos = get_airports_from_date('test_data.csv', date)
		for airport, flight_infos in airport_to_flight_infos.items():
			total_delay += sum([flight_info.delay() for flight_info in flight_infos])
			total_p += sum([1 if flight_info.delayed() else 0 for flight_info in flight_infos])
			total_flights += len(flight_infos)
	print 'total_flights', total_flights
	print 'avg_delay', float(total_delay)/total_flights
	print 'avg_p', float(total_p)/total_flights

# returns the avg delays of an airport
def avg_delay(flight_infos):
	assert isinstance(flight_infos, list)
	return float(sum([flight_info.delay() for flight_info in flight_infos]))/len(flight_infos)

# returns the intervals from flight_infos
def intervals(flight_infos):
	return [Interval(flight_info) for flight_info in flight_infos]